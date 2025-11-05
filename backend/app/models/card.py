from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Card:
    """Modelo para representar uma carta MTG"""
    name: str
    set_name: str
    mana_cost: Optional[str] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    rarity: Optional[str] = None
    scryfall_uri: Optional[str] = None
    image_uris: Optional[Dict] = None
    colors: Optional[List[str]] = None
    
    def to_dict(self):
        """Converte o objeto Card para dicionário"""
        return {
            'name': self.name,
            'set': self.set_name,
            'mana_cost': self.mana_cost,
            'type_line': self.type_line,
            'oracle_text': self.oracle_text,
            'rarity': self.rarity,
            'scryfall_uri': self.scryfall_uri,
            'image_uris': self.image_uris or {},
            'colors': self.colors or []
        }
    
    @classmethod
    def from_scryfall_data(cls, scryfall_data: dict):
        """Cria um objeto Card a partir dos dados do Scryfall"""
        return cls(
            name=scryfall_data.get('name', ''),
            set_name=scryfall_data.get('set_name', ''),
            mana_cost=scryfall_data.get('mana_cost'),
            type_line=scryfall_data.get('type_line'),
            oracle_text=scryfall_data.get('oracle_text'),
            rarity=scryfall_data.get('rarity'),
            scryfall_uri=scryfall_data.get('scryfall_uri'),
            image_uris=scryfall_data.get('image_uris', {}),
            colors=scryfall_data.get('colors', [])
        )
