from pathlib import Path # To create and manipulate folders
import unicodedata # to manipulate names

class Tools:
    
    @staticmethod
    def remove_accents(text: str) -> str:
        
        """
        Remove accents from a string.

        Args:
            text (str): Input string potentially containing accents.

        Returns:
            str: String with accents removed.
        """
    
        normalized = unicodedata.normalize("NFD", text) # separated for example è into e`
        return "".join(c for c in normalized if unicodedata.category(c) != "Mn") # picks out all the accents
    
    def folder_exists(path: str, folder_name: str) -> bool:
        """
        Check if a folder with a certain name exists in the BASE_PATH.

        Args:
            path (str): Path to the directory where to look.
            folder_name (str): Name of the folder to check.

        Returns:
            bool: True if the folder exists, False otherwise.
        """
        target_folder = path / folder_name  # build full path
        return target_folder.is_dir()  # returns True if it exists and is a directory

class Family:
    def __init__(
        self,
        fn_dad: str,
        ln_dad: str,
        fn_mom: str,
        ln_mom: str,
        children_list: list[str]
    ):
        
        self.fn_dad = fn_dad
        self.ln_dad = ln_dad
        self.fn_mom = fn_mom
        self.ln_mom = ln_mom
        self.children_list = children_list
        self.folder_name = self._generate_folder_name()
        
    def _generate_folder_name(self):
        """
        builds the name of the folder in the format:
        [first_name_father][LAST_NAME_FATHER]_[first_name_mother][LAST_NAME_MOTHER]
        with accents removed.
            
        Returns:
            str: Folder name formatted and accent-free.
        """
        dad_part = Tools.remove_accents(self.fn_dad).lower() + Tools.remove_accents(self.ln_dad).upper()
        mom_part = Tools.remove_accents(self.fn_mom).lower() + Tools.remove_accents(self.ln_mom).upper()
        return f"{dad_part}_{mom_part}"
    
    def build_folder(self,path) -> None:
    
        """
        builds the following structure:
        
        [first_name_father][LAST_NAME_FATHER]_[first_name_mother][LAST_NAME_MOTHER]/
        ├── family/
        │   ├── documents/
        │   └── images/
        ├── [first_name_child1][LAST_NAME_FATHER]L/
        │   ├── documents/
        │   └── images/
        └── [first_name_child2][LAST_NAME_FATHER]/
            ├── documents/
            └── images/
        """
        if Tools.folder_exists(path,self.folder_name):
            print(f"Folder {self.folder_name} already exists.")
        else:
            for name in ["family"]+[ (Tools.remove_accents(child_name.lower() + self.ln_dad.upper())) for child_name in self.children_list]:
                for subname in ["documents","images"]:
                    folder_path = path / self.folder_name / Path(name) / Path(subname)
                    folder_path.mkdir(parents = True)