import pyodbc
import logging
import inspect

# Classe représentant un contact.
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        """Initialise un contact avec le nom, prénom, email et téléphone."""
        self._nom = nom
        self._prenom = prenom
        self._email = email
        self._telephone = telephone

    def __str__(self):
        """Retourne une représentation sous forme de chaîne du contact."""
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Email: {self.email}, Téléphone: {self.telephone}"

    # Getters pour accéder aux attributs privés
    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def email(self):
        return self._email

    @property
    def telephone(self):
        return self._telephone

    # Setters pour modifier les attributs privés
    @nom.setter
    def nom(self, nom):
        self._nom = nom

    @prenom.setter
    def prenom(self, prenom):
        self._prenom = prenom

    @email.setter
    def email(self, email):
        self._email = email

    @telephone.setter
    def telephone(self, telephone):
        self._telephone = telephone


# Classe pour gérer les contacts.
class GestionnaireContact:
    def __init__(self):
        """Initialise le gestionnaire de contacts et crée la table si elle n'existe pas."""
        self.contacts = []  # Liste des contacts en mémoire
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ZAKARIA_LAPTOP;'  
            'DATABASE=Gestion_Contacts;'  
            'Trusted_Connection=yes;'
        )
        self.create_table()  # Appel de la méthode pour créer la table

    def connect_db(self):
        """Établit une connexion à la base de données et retourne l'objet de connexion."""
        print("connected")
        return pyodbc.connect(self.connection_string)

    def create_table(self):
        """Crée la table Contacts dans la base de données si elle n'existe pas déjà."""
        create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Contacts' AND xtype='U')
        CREATE TABLE Contacts (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            Nom NVARCHAR(100),
            Prenom NVARCHAR(100),
            Email NVARCHAR(100),
            Telephone NVARCHAR(15)
        );
        """
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    def ajouter_contact(self):
        """Ajoute un nouveau contact à la base de données après validation des données saisies."""
        while True:
            nom = input("Entrez le nom: ")
            if not nom.isalpha():
                print("Le nom doit contenir uniquement des lettres.")
                continue
            break

        while True:
            prenom = input("Entrez le prénom: ")
            if not prenom.isalpha():
                print("Le prénom doit contenir uniquement des lettres.")
                continue
            break

        while True:
            email = input("Entrez l'email: ")
            # Ajouter une validation d'email si nécessaire
            break

        while True:
            telephone = input("Entrez le téléphone: ")
            if not telephone.isdigit():
                print("Le téléphone doit contenir uniquement des chiffres.")
                continue
            break

        # Requête d'insertion d'un contact dans la base de données
        insert_query = """
        INSERT INTO [Contacts] (Nom, Prenom, Email, Telephone)
        VALUES (?, ?, ?, ?);
        """
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (nom, prenom, email, telephone))
            conn.commit()
        logging.info(f"Contact ajouté : {nom} {prenom}")

    def afficher_contacts(self):
        """Affiche tous les contacts enregistrés dans la base de données."""
        select_query = "SELECT * FROM Contacts;"

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            rows = cursor.fetchall()
            if not rows:
                print("Aucun contact à afficher.")
            else:
                for row in rows:
                    print(f"Nom: {row.Nom}, Prénom: {row.Prenom}, Email: {row.Email}, Téléphone: {row.Telephone}")

    def rechercher_contact(self, nom):
        """Recherche un contact par nom et affiche les résultats ou retourne les détails du contact pour modification ou suppression."""
        select_query = "SELECT * FROM Contacts WHERE Nom = ?;"
        caller = inspect.stack()[1].function  # Déterminer la fonction appelante
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (nom,))
            results = cursor.fetchall()

        if results:
            logging.info(f"{len(results)} contact(s) trouvé(s) pour le nom '{nom}'.")
            for row in results:
                if caller == "modifier_contact":
                    return results
                elif caller == "supprimer_contact":
                    return results[0].Id, results
                else:
                    print(f"Nom: {row.Nom}, Prénom: {row.Prenom}, Email: {row.Email}, Téléphone: {row.Telephone}")
        else:
            print(f"Aucun contact trouvé pour le nom '{nom}'.")

    def modifier_contact(self, nom):
        """Modifie les détails d'un contact existant après avoir demandé l'ID du contact."""
        contacts_a_modifier = self.rechercher_contact(nom)
        Ids = []
        if not contacts_a_modifier:
            logging.error(f"Contact avec le nom '{nom}' introuvable pour modification.")
            return
        if len(contacts_a_modifier) > 1:
            print("Plusieurs contacts trouvés :")
            for row in contacts_a_modifier:
                print(f"Id: {row.Id}, Nom: {row.Nom}, Prénom: {row.Prenom}, Email: {row.Email}, Téléphone: {row.Telephone}")
                Ids.append(row.Id)
            while True:
                try:
                    Id = int(input("Entrez l'ID du contact que vous voulez modifier (1, 2, ...): "))
                    if Id in Ids:
                        break
                    else:
                        logging.error("\nChoix hors de portée. Veuillez réessayer.\n")
                except ValueError:
                    logging.error("Entrée invalide. Veuillez entrer un numéro.")

        nouveau_nom = input(f"Nouveau nom : ")
        nouveau_prenom = input(f"Nouveau prénom : ")
        nouveau_email = input(f"Nouveau email: ")
        nouveau_telephone = input(f"Nouveau téléphone : ")

        # Requête de mise à jour des détails du contact
        update_query = """
        UPDATE Contacts
        SET Nom = ?, Prenom = ?, Email = ?, Telephone = ?
        WHERE Id = ?;
        """

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(update_query, (nouveau_nom, nouveau_prenom, nouveau_email, nouveau_telephone, Id))
            conn.commit()
            logging.info(f"Contact modifié: {nouveau_nom} {nouveau_prenom}")

    def supprimer_contact(self, nom):
        """Supprime un contact existant en demandant à l'utilisateur d'entrer l'ID du contact à supprimer."""
        Id, contacts_a_sup = self.rechercher_contact(nom)
        Ids = []
        if not contacts_a_sup:
            logging.error(f"Contact avec le nom '{nom}' introuvable pour suppression.")
            return

        if len(contacts_a_sup) > 1:
            print("Plusieurs contacts trouvés :")
            for row in contacts_a_sup:
                print(f"Id: {row.Id}, Nom: {row.Nom}, Prénom: {row.Prenom}, Email: {row.Email}, Téléphone: {row.Telephone}")
                Ids.append(row.Id)
            while True:
                try:
                    Id = int(input("Entrez l'ID du contact que vous voulez supprimer (1, 2, ...): "))
                    if Id in Ids:
                        break
                    else:
                        logging.error("Choix hors de portée. Veuillez réessayer.")
                except ValueError:
                    logging.error("Entrée invalide. Veuillez entrer un numéro.")

        delete_query = "DELETE FROM Contacts WHERE Id = ?;"
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(delete_query, (Id,))
            conn.commit()
            logging.info(f"Contact supprimé: {nom}")


# Classe principale pour exécuter le programme
class Main:
    def __init__(self):
        """Initialise l'application et crée une instance du gestionnaire de contacts."""
        self.gestionnaire = GestionnaireContact()

    def main(self):
        """Boucle principale de l'application permettant à l'utilisateur de choisir les actions à effectuer."""
        while True:
            print("\nGestionnaire de Contacts")
            print("1. Ajouter un contact")
            print("2. Consulter la liste des contacts")
            print("3. Rechercher un contact")
            print("4. Modifier un contact")
            print("5. Supprimer un contact")
            print("6. Quitter")
            choix = input("Choisissez une option: ")

            if choix == "1":
                self.gestionnaire.ajouter_contact()
            elif choix == "2":
                self.gestionnaire.afficher_contacts()
            elif choix == "3":
                self.gestionnaire.rechercher_contact(input("Entrez le nom du contact: "))
            elif choix == "4":
                self.gestionnaire.modifier_contact(input("Entrez le nom de contact : "))
            elif choix == "5":
                self.gestionnaire.supprimer_contact(input('Entrez le nom de contact: '))
            elif choix == "6":
                print("Au revoir!")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    app = Main()
    app.main()
