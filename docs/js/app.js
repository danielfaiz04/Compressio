// Language translations
const translations = {
    en: {
        title: 'Compressio',
        tagline: 'Smarter, Smaller, Simpler',
        dragDrop: 'Drag & Drop Files Here',
        or: 'or',
        chooseFiles: 'Choose Files',
        recentCompressions: 'Recent Compressions',
        fileName: 'File Name',
        originalSize: 'Original Size',
        compressedSize: 'Compressed Size',
        ratio: 'Ratio',
        action: 'Action',
        download: 'Download',
        login: 'Login',
        logout: 'Logout',
        home: 'Home',
        about: 'About',
        compressing: 'Compressing',
        compressionSuccess: 'File compressed successfully!',
        compressionFailed: 'Compression failed. Please try again.',
        downloadFailed: 'Download failed. Please try again.',
        invalidFileType: 'Invalid file type. Please upload JPG, PNG, or TXT files.',
        limitReached: 'Compression limit reached. Please login for unlimited access.',
        loginSuccess: 'Successfully logged in!',
        loginFailed: 'Login failed. Please try again.',
        logoutSuccess: 'Successfully logged out!',
        logoutFailed: 'Logout failed. Please try again.',
        online: 'You are back online!',
        offline: 'You are offline. Some features may not work.',
        
        // About Page Translations
        aboutTitle: 'About Compressio',
        aboutTagline: 'A modern web application for file compression',
        whatIsCompressio: 'What is Compressio?',
        whatIsCompressioText: 'Compressio is a web-based file compression application that allows users to compress and decompress files with a clean, user-friendly interface. The application features Firebase Authentication for secure access and session-based compression limits.',
        featuresTitle: 'Features',
        fileCompressionTitle: 'File Compression',
        fileCompressionText: 'Compress various file types including images and documents using different algorithms.',
        googleSignInTitle: 'Google Sign-In',
        googleSignInText: 'Secure authentication using Firebase and Google Sign-In.',
        compressionHistoryTitle: 'Compression History',
        compressionHistoryText: 'View your recent compression activities and download results.',
        multipleAlgorithmsTitle: 'Multiple Algorithms',
        multipleAlgorithmsText: 'Choose between Huffman coding and Run-Length Encoding based on your needs.',
        supportedFilesTitle: 'Supported File Types',
        imagesTitle: 'Images',
        documentsTitle: 'Documents',
        techStackTitle: 'Technology Stack',
        frontendTitle: 'Frontend',
        backendTitle: 'Backend'
    },
    id: {
        title: 'Compressio',
        tagline: 'Lebih Pintar, Lebih Kecil, Lebih Sederhana',
        dragDrop: 'Seret & Lepas File Di Sini',
        or: 'atau',
        chooseFiles: 'Pilih File',
        recentCompressions: 'Kompresi Terbaru',
        fileName: 'Nama File',
        originalSize: 'Ukuran Asli',
        compressedSize: 'Ukuran Terkompresi',
        ratio: 'Rasio',
        action: 'Aksi',
        download: 'Unduh',
        login: 'Masuk',
        logout: 'Keluar',
        home: 'Beranda',
        about: 'Tentang',
        compressing: 'Mengompres',
        compressionSuccess: 'File berhasil dikompres!',
        compressionFailed: 'Kompresi gagal. Silakan coba lagi.',
        downloadFailed: 'Unduhan gagal. Silakan coba lagi.',
        invalidFileType: 'Tipe file tidak valid. Silakan unggah file JPG, PNG, atau TXT.',
        limitReached: 'Batas kompresi tercapai. Silakan masuk untuk akses tak terbatas.',
        loginSuccess: 'Berhasil masuk!',
        loginFailed: 'Gagal masuk. Silakan coba lagi.',
        logoutSuccess: 'Berhasil keluar!',
        logoutFailed: 'Gagal keluar. Silakan coba lagi.',
        online: 'Anda kembali online!',
        offline: 'Anda sedang offline. Beberapa fitur mungkin tidak berfungsi.',
        
        // About Page Translations (Bahasa Indonesia)
        aboutTitle: 'Tentang Compressio',
        aboutTagline: 'Aplikasi web modern untuk kompresi file',
        whatIsCompressio: 'Apa itu Compressio?',
        whatIsCompressioText: 'Compressio adalah aplikasi kompresi file berbasis web yang memungkinkan pengguna untuk mengkompres dan mendekompilasi file dengan antarmuka yang bersih dan mudah digunakan. Aplikasi ini dilengkapi dengan Autentikasi Firebase untuk akses aman dan batasan kompresi berbasis sesi.',
        featuresTitle: 'Fitur',
        fileCompressionTitle: 'Kompresi File',
        fileCompressionText: 'Kompres berbagai jenis file termasuk gambar dan dokumen menggunakan algoritma yang berbeda.',
        googleSignInTitle: 'Masuk dengan Google',
        googleSignInText: 'Autentikasi aman menggunakan Firebase dan Masuk dengan Google.',
        compressionHistoryTitle: 'Riwayat Kompresi',
        compressionHistoryText: 'Lihat aktivitas kompresi terbaru Anda dan unduh hasilnya.',
        multipleAlgorithmsTitle: 'Berbagai Algoritma',
        multipleAlgorithmsText: 'Pilih antara Huffman coding dan Run-Length Encoding berdasarkan kebutuhan Anda.',
        supportedFilesTitle: 'Jenis File yang Didukung',
        imagesTitle: 'Gambar',
        documentsTitle: 'Dokumen',
        techStackTitle: 'Tumpukan Teknologi',
        frontendTitle: 'Frontend',
        backendTitle: 'Backend',
        technologyUsedTitle: 'Teknologi yang Digunakan',
        
        // How to Use Page Translations
        howToUseTitle: 'Cara Menggunakan Compressio',
        step1: 'Unggah File Anda: Seret dan lepaskan file Anda ke area yang ditentukan atau klik "Pilih File" untuk memilihnya dari perangkat Anda.',
        step2: 'Pilih Jenis Kompresi: Pilih antara "Kompres" atau "Dekompresi" berdasarkan kebutuhan Anda.',
        step3: 'Pilih Algoritma (Opsional): Pilih algoritma kompresi pilihan Anda. Otomatis (secara otomatis memilih algoritma terbaik untuk file Anda), Huffman Coding (metode efisien untuk kompresi data lossless), atau Run-Length Encoding (bentuk kompresi data di mana urutan data disimpan sebagai nilai data tunggal dan hitungan).',
        step4: 'Proses File: Klik tombol "Proses File" untuk memulai kompresi atau dekompresi.',
        step5: 'Unduh Hasil: Setelah diproses, file yang dikompres/didekompres akan muncul di tabel "Kompresi Terbaru". Klik "Unduh" untuk menyimpannya.'
    }
};

// Language switcher
document.getElementById('languageSelect').addEventListener('change', (e) => {
    const lang = e.target.value;
    localStorage.setItem('preferredLanguage', lang);
    updateLanguage(lang);
});

// Update language
function updateLanguage(lang) {
    const t = translations[lang];
    
    // Update static text (Removed direct selectors - now handled by data-translate-key)
    // document.querySelector('h1').textContent = t.title;
    // document.querySelector('.lead').textContent = t.tagline;
    
    // Updated selectors for dropZone based on new HTML structure (Removed direct selectors)
    // const dropZoneH3 = document.querySelector('#dropZone h3');
    // if (dropZoneH3) dropZoneH3.textContent = t.dragDrop;
    
    // const dropZoneP = document.querySelector('#dropZone p');
    // if (dropZoneP) dropZoneP.textContent = t.or;
    
    // const dropZoneButton = document.querySelector('#dropZone button');
    // if (dropZoneButton) dropZoneButton.textContent = t.chooseFiles;

    // document.querySelector('.card-header h5').textContent = t.recentCompressions; // Assuming this is the history header (Removed direct selectors)
    
    // Update table headers (Removed direct selectors)
    // const headers = document.querySelectorAll('#historyTable th');
    // if (headers[0]) headers[0].textContent = t.fileName;
    // if (headers[1]) headers[1].textContent = t.originalSize;
    // if (headers[2]) headers[2].textContent = t.compressedSize;
    // if (headers[3]) headers[3].textContent = t.ratio;
    // if (headers[4]) headers[4].textContent = t.action;
    
    // Update navigation
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.textContent =
            firebase.auth().currentUser ? t.logout : t.login;
    }
    const aboutLink = document.querySelector('a[href="about.html"]');
    if (aboutLink) {
        aboutLink.textContent = t.about;
    }
    
    // Update download buttons (dynamically added, so update when history renders)
    // This part might be better handled in updateHistoryTable of compress.js
    // document.querySelectorAll('#historyTable .btn').forEach(btn => {
    //     btn.textContent = t.download;
    // });

    // Update About Page elements (This loop will now handle all translations)
    const elementsToTranslate = document.querySelectorAll('[data-translate-key]');
    console.log('Elements to translate found:', elementsToTranslate.length);
    elementsToTranslate.forEach(element => {
        const key = element.getAttribute('data-translate-key');
        if (t[key]) {
            element.textContent = t[key];
        }
    });
}

// Handle page visibility
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        // Refresh compression history when page becomes visible
        fileCompressor.loadCompressionHistory();
    }
});

// Handle offline/online status
window.addEventListener('online', () => {
    showToast('You are back online!', 'success');
});

window.addEventListener('offline', () => {
    showToast('You are offline. Some features may not work.', 'warning');
});

// Constants
const MAX_COMPRESSIONS = 5;
const API_BASE_URL = 'https://compressio-production.up.railway.app';

// State management
let compressionHistory = JSON.parse(localStorage.getItem('compressionHistory') || '[]');

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const compressionType = document.getElementById('compressionType');
const historyTable = document.getElementById('historyTable'); // Corrected from historyList
const selectedFileNameDisplay = document.getElementById('selectedFileName');
const fileNameSpan = document.getElementById('fileNameDisplay');
const clearFileBtn = document.getElementById('clearFileSelection');
const processFileButton = document.querySelector('#uploadForm button[type="submit"]');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    // renderHistory() is now handled by fileCompressor.loadCompressionHistory();
});

// Initialize application
function initializeApp() {
    // Set up file input change handler
    fileInput.addEventListener('change', handleFileSelect);
    
    // Set up form submit handler
    uploadForm.addEventListener('submit', handleFormSubmit);

    // Set up clear file selection button
    if (clearFileBtn) {
        clearFileBtn.addEventListener('click', clearFileSelection);
    }
    
    // Set up drag and drop
    const dropZone = document.getElementById('dropZone'); // Get dropZone by ID
    if (dropZone) {
        dropZone.addEventListener('dragover', handleDragOver);
        dropZone.addEventListener('dragleave', handleDragLeave);
        dropZone.addEventListener('drop', handleDrop);
        // Add click event for dropZone to trigger file input click
        dropZone.addEventListener('click', () => fileInput.click());
    }

    // Initial state for process button
    processFileButton.disabled = true; 

    // Initialize language update on load (Consolidated here)
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'id';
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = preferredLanguage;
        updateLanguage(preferredLanguage); // Call updateLanguage here
        languageSelect.addEventListener('change', (e) => {
            const lang = e.target.value;
            localStorage.setItem('preferredLanguage', lang);
            updateLanguage(lang);
        });
    }
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displaySelectedFile(file.name);
    } else {
        clearFileSelection();
    }
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    const file = fileInput.files[0];
    if (file) {
        const operation = document.querySelector('input[name="operation"]:checked').value;
        if (validateCompressionSettings(file, compressionType.value, operation)) {
             // Use fileCompressor from compress.js to handle the actual logic
            fileCompressor.handleFiles([file], operation); 
        }
    } else {
        showToast('Please select a file', 'warning');
    }
}

// Handle drag and drop
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('dragover');
    
    const file = event.dataTransfer.files[0];
    if (file) {
        displaySelectedFile(file.name);
    }
}

// Function to display the selected file name
function displaySelectedFile(fileName) {
    fileNameSpan.textContent = fileName;
    selectedFileNameDisplay.style.display = 'block';
    processFileButton.disabled = false; // Enable process button
}

// Function to clear the selected file
function clearFileSelection() {
    fileInput.value = ''; // Clear the file input
    fileNameSpan.textContent = '';
    selectedFileNameDisplay.style.display = 'none';
    processFileButton.disabled = true; // Disable process button
}

// Moved from compress.js to app.js to consolidate file handling
function validateCompressionSettings(file, compressionType, operation) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    // Check if file type is supported for the selected compression type
    if (compressionType === COMPRESSION_TYPES.HUFFMAN && !['.png', '.jpg', '.jpeg'].includes(ext)) {
        showToast('Huffman compression only supports image files', 'warning');
        return false;
    }
    
    if (compressionType === COMPRESSION_TYPES.RLE && !['.txt', '.pdf'].includes(ext)) {
        showToast('RLE compression only supports text and PDF files', 'warning');
        return false;
    }
    
    // Check if operation is valid for the file
    if (operation === 'decompress') {
        // Allow decompressing any file type, but optionally warn if not a 'compressed_' file
        // The backend handles the actual decompression logic based on algorithm
        // if (!file.name.startsWith('compressed_') && !file.name.startsWith('decompressed_')) {
        //     showToast('This file does not appear to be a compressed file', 'warning');
        //     // return false; // Decide if this should strictly prevent decompression
        // }
    }
    
    return true;
}

// Constants for compression types (moved from compress.js for validation logic)
const COMPRESSION_TYPES = {
    AUTO: 'auto',
    HUFFMAN: 'huffman',
    RLE: 'rle'
};

// Show/hide loading state
function showLoading(show) {
    const submitBtn = uploadForm.querySelector('button[type="submit"]');
    if (show) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Process File';
    }
}

// Format file size
function formatSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    
    return `${size.toFixed(2)} ${units[unitIndex]}`;
} 