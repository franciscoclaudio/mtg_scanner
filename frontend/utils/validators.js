export class Validators {
    static validateImageFile(file, maxSizeMB = 10) {
        const errors = [];
        
        if (!file) {
            errors.push('Nenhum arquivo selecionado');
            return errors;
        }

        // Verifica tipo do arquivo
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp'];
        if (!allowedTypes.includes(file.type)) {
            errors.push('Tipo de arquivo não suportado. Use JPEG, PNG, GIF ou BMP.');
        }

        // Verifica tamanho do arquivo
        const maxSizeBytes = maxSizeMB * 1024 * 1024;
        if (file.size > maxSizeBytes) {
            errors.push(`Arquivo muito grande. Tamanho máximo: ${maxSizeMB}MB`);
        }

        if (file.size === 0) {
            errors.push('Arquivo vazio');
        }

        return errors;
    }

    static validateOutputFilename(filename) {
        const errors = [];
        
        if (!filename) {
            errors.push('Nome do arquivo de saída é obrigatório');
            return errors;
        }

        if (!filename.toLowerCase().endsWith('.txt')) {
            errors.push('O arquivo de saída deve ter extensão .txt');
        }

        // Verifica caracteres inválidos no nome do arquivo
        const invalidChars = /[<>:"/\\|?*]/;
        if (invalidChars.test(filename)) {
            errors.push('Nome do arquivo contém caracteres inválidos');
        }

        if (filename.length > 255) {
            errors.push('Nome do arquivo muito longo');
        }

        return errors;
    }

    static sanitizeFilename(filename) {
        // Remove caracteres inválidos e espaços extras
        return filename
            .replace(/[<>:"/\\|?*]/g, '_')
            .replace(/\s+/g, ' ')
            .trim();
    }
}
