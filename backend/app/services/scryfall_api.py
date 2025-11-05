import requests
import time
import json
from datetime import datetime
from ...utils.config import Config

class ScryfallService:
    def __init__(self):
        self.base_url = Config.SCRYFALL_API_URL
        self.rate_limit_delay = Config.SCRYFALL_RATE_LIMIT_DELAY
        self.cache_file = Config.CARD_CACHE_FILE
        self.cache = self._load_cache()
    
    def _load_cache(self):
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def search_card_by_name(self, card_name, exact=True):
        """Busca carta pelo nome no Scryfall"""
        if not card_name:
            return None
        
        # Verifica cache primeiro
        cache_key = f"{card_name.lower()}_{'exact' if exact else 'fuzzy'}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            # Verifica se o cache não expirou
            cache_time = datetime.fromisoformat(cached_data['cached_at'])
            if (datetime.now() - cache_time).days < 7:
                return cached_data['data']
        
        try:
            if exact:
                response = requests.get(f"{self.base_url}/cards/named?exact={card_name}")
            else:
                response = requests.get(f"{self.base_url}/cards/named?fuzzy={card_name}")
            
            if response.status_code == 200:
                card_data = response.json()
                
                # Salva no cache
                self.cache[cache_key] = {
                    'data': card_data,
                    'cached_at': datetime.now().isoformat()
                }
                self._save_cache()
                
                return card_data
            
            return None
            
        except requests.RequestException as e:
            print(f"Erro na requisição Scryfall: {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)
    
    def search_cards_by_text(self, text):
        """Busca múltiplas cartas baseado no texto extraído"""
        if not text:
            return []
        
        lines = text.split('\n')
        potential_names = []
        
        for line in lines:
            line = line.strip()
            if self._is_potential_card_name(line):
                potential_names.append(line)
        
        cards_found = []
        
        for name in potential_names[:5]:  # Limita para performance
            card_data = self.search_card_by_name(name, exact=False)
            if card_data:
                cards_found.append(self._format_card_data(card_data))
        
        return cards_found
    
    def _is_potential_card_name(self, text):
        """Verifica se o texto parece ser um nome de carta"""
        if len(text) < 3 or len(text) > 50:
            return False
        
        # Palavras comuns que geralmente não são nomes de cartas
        common_words = {'mana', 'cost', 'tap', 'attack', 'defense', 'life', 'card', 'hand'}
        if any(word in text.lower() for word in common_words):
            return False
        
        # Remove linhas que parecem ser texto de regras
        if any(char.isdigit() for char in text) and not text[0].isupper():
            return False
        
        return True
    
    def _format_card_data(self, card_data):
        """Formata os dados da carta para resposta padronizada"""
        return {
            'name': card_data.get('name'),
            'set': card_data.get('set_name'),
            'mana_cost': card_data.get('mana_cost', ''),
            'type_line': card_data.get('type_line', ''),
            'oracle_text': card_data.get('oracle_text', ''),
            'rarity': card_data.get('rarity', ''),
            'scryfall_uri': card_data.get('scryfall_uri', ''),
            'image_uris': card_data.get('image_uris', {}),
            'colors': card_data.get('colors', [])
        }
