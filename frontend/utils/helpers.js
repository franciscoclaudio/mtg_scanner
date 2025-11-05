export class Helpers {
    static generateFilename(originalName, suffix = '_decklist') {
        if (!originalName) return 'decklist.txt';
        
        // Remove a extensão do arquivo original
        const baseName = originalName.replace(/\.[^/.]+$/, "");
        // Adiciona sufixo e extensão .txt
        return `${baseName}${suffix}.txt`;
    }

    static validateFileType(file, allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']) {
        return file && allowedTypes.includes(file.type);
    }

    static formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}
