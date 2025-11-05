class UIManager {
    constructor() {
        this.statusElement = document.getElementById('statusMessage');
        this.resultsArea = document.getElementById('resultsArea');
        this.cardList = document.getElementById('cardList');
    }

    showStatus(message, type = 'info') {
        const typeClasses = {
            info: 'bg-blue-100 text-blue-800 border-blue-400',
            loading: 'bg-yellow-100 text-yellow-800 border-yellow-400',
            success: 'bg-green-100 text-green-800 border-green-600',
            error: 'bg-red-100 text-red-800 border-red-600'
        };

        this.statusElement.textContent = message;
        this.statusElement.className = `mt-6 p-3 rounded-lg text-sm border-l-4 ${typeClasses[type]}`;
        this.statusElement.classList.remove('hidden');
    }

    hideStatus() {
        this.statusElement.classList.add('hidden');
    }

    showResults(cards) {
        this.cardList.innerHTML = '';
        
        cards.forEach(card => {
            const cardElement = this.createCardElement(card);
            this.cardList.appendChild(cardElement);
        });

        this.resultsArea.classList.remove('hidden');
    }

    createCardElement(card) {
        const li = document.createElement('li');
        li.className = 'p-3 bg-white rounded-lg border border-gray-200';
        
        li.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <h4 class="font-semibold text-mtg-brown">${card.name}</h4>
                    <p class="text-sm text-gray-600">${card.type_line} • ${card.set}</p>
                    <p class="text-xs text-gray-500">${card.mana_cost || 'Sem custo de mana'}</p>
                </div>
                <span class="px-2 py-1 text-xs rounded-full bg-gray-100">${card.rarity}</span>
            </div>
        `;
        
        return li;
    }

    showLoading(button) {
        button.disabled = true;
        button.innerHTML = `
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processando...
        `;
    }

    hideLoading(button) {
        button.disabled = false;
        button.textContent = 'Listar Cards';
    }

    triggerDownload(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }
}
