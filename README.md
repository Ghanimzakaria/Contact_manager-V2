Documentation
1. Classe Contact
Description: Représente un contact avec des attributs pour le nom, le prénom, l'email et le téléphone. Fournit des getters et des setters pour la gestion des données.
Méthodes:
__init__(self, nom, prenom, email, telephone): Initialise un nouveau contact.
__str__(self): Retourne une représentation sous forme de chaîne du contact.
2. Classe GestionnaireContact
Description: Gère les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) sur les contacts. Établit une connexion à une base de données SQL Server.
Méthodes:
__init__(self): Initialise le gestionnaire et crée la table des contacts si nécessaire.
connect_db(self): Établit et retourne une connexion à la base de données.
create_table(self): Crée la table Contacts dans la base de données.
ajouter_contact(self): Ajoute un nouveau contact à la base de données.
afficher_contacts(self): Affiche tous les contacts de la base de données.
rechercher_contact(self, nom): Recherche un contact par nom.
modifier_contact(self, nom): Modifie les détails d'un contact existant.
supprimer_contact(self, nom): Supprime un contact existant.
3. Classe Main
Description: Point d'entrée de l'application, gère l'interaction avec l'utilisateur.
Méthodes:
__init__(self): Initialise l'application.
main(self): Boucle principale qui permet à l'utilisateur de choisir des actions à effectuer.
Commentaires
Logique: La gestion des erreurs est intégrée à chaque méthode pour valider les entrées de l'utilisateur.
Simplicité: Les entrées utilisateur sont traitées dans des boucles while pour garantir que les données saisies sont valides.
