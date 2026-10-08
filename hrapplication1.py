import json
import os

FILE_NAME = "applications.json"


class ApplicationError(Exception):
    pass


class UnauthorizedError(ApplicationError):
    pass


class Application:
    def __init__(self, application_id, candidate_id, name, email, role):
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.name = name
        self.email = email
        self.role = role

    def to_dict(self):

        return {
            "application_id": self.application_id,
            "candidate_id": self.candidate_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["application_id"],
            data["candidate_id"],
            data["name"],
            data["email"],
            data["role"],
        )

    def show_details(self):

        print("\n-----------------------------")
        print("Application ID:", self.application_id)
        print("Candidate ID:", self.candidate_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Role:", self.role)
        print("-----------------------------")


class FileManager:
    @staticmethod
    def create_file_if_not_exists():

        try:
            if not os.path.exists(FILE_NAME):
                with open(FILE_NAME, "w") as file:
                    json.dump([], file, indent=4)

        except Exception as e:
            print("Error creating file:", e)

    @staticmethod
    def load_applications():

        try:
            FileManager.create_file_if_not_exists()

            with open(FILE_NAME, "r") as file:
                data = json.load(file)

            applications = []

            for item in data:
                application = Application.from_dict(item)

                applications.append(application)

            return applications

        except Exception as e:
            print("Error loading applications:", e)

            return []

    @staticmethod
    def save_applications(applications):

        try:
            data = []

            for application in applications:
                data.append(application.to_dict())

            with open(FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)

            print("Application saved successfully.")

        except Exception as e:
            print("Error saving applications:", e)


class ApplicationManager:
    def __init__(self):

        self.applications = FileManager.load_applications()

    def add_application(self):

        try:
            print("\n----- Add Application -----")

            application_id = input("Enter Application ID: ")

            candidate_id = input("Enter Candidate ID: ")

            name = input("Enter Candidate Name: ")

            email = input("Enter Email: ")

            role = input("Enter Role: ")

            application = Application(application_id, candidate_id, name, email, role)

            self.applications.append(application)

            FileManager.save_applications(self.applications)

        except Exception as e:
            print("Error:", e)

    def hr_view_applications(self):

        try:
            if len(self.applications) == 0:
                print("\nNo applications found.")

                return

            print("\n===== ALL APPLICATIONS =====")

            for application in self.applications:
                application.show_details()

        except Exception as e:
            print("Error:", e)

    def candidate_view_application(self):

        try:
            print("\n----- Candidate View -----")

            candidate_id = input("Enter your Candidate ID: ")

            application_id = input("Enter Application ID: ")

            for application in self.applications:
                if application.application_id == application_id:
                    if application.candidate_id != candidate_id:
                        raise UnauthorizedError(
                            "You cannot view another candidate's application."
                        )

                    application.show_details()

                    return

            print("Application not found.")

        except UnauthorizedError as e:
            print("Access Denied:", e)

        except Exception as e:
            print("Error:", e)


def main():

    manager = ApplicationManager()

    while True:
        print("\n==============================")
        print("   HR APPLICATION MANAGER")
        print("==============================")

        print("1. Add Application")
        print("2. HR - View All Applications")
        print("3. Candidate - View Application")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            manager.add_application()

        elif choice == "2":
            manager.hr_view_applications()

        elif choice == "3":
            manager.candidate_view_application()

        elif choice == "4":
            print("Program ended.")

            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
