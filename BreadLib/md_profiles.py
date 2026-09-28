from dataclasses import dataclass
from yaml import safe_load
from .md_notif import *
all_profiles = []

@dataclass(frozen=True) # <- frozen means readonly
class Profile:
    name: str
    columns: int
    startRow: int
    maxEmptyRows: int
    referenceColumn: int
    materialColumn: int
    countColumn: int
    week_order: list[str]

def loadProfilesYaml(path, registry):
        with open(path, 'r',) as file:
            config = safe_load(file)
        for profile_dict in config["profiles"]:
            profile = Profile(**profile_dict)
            registry.register(profile)     

class ProfileRegistry:
    def __init__(self):
        self._profiles: list[Profile] = []

    def register(self, profile:Profile) -> Profile: # -> Like in F# means return type
        if profile in self._profiles:
            msg_warning(f"{profile.name} is already registered!")
        self._profiles.append(profile)
        msg_info(f"Profile {profile.name} was added!")
        return profile

    def get_all(self) -> list[Profile]:
        return self._profiles

registry = ProfileRegistry()
loadProfilesYaml("profiles.yaml", registry)