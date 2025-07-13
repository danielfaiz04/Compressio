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
        method: 'Method',
        action: 'Action',
        download: 'Download',
        compare: 'Compare',
        delete: 'Delete',
        login: 'Login',
        logout: 'Logout',
        home: 'Home',
        about: 'About',
        compressing: 'Compressing',
        compressionSuccess: 'File compressed successfully!',
        compressionFailed: 'Compression failed. Please try again.',
        downloadFailed: 'Download failed. Please try again.',
        invalidFileType: 'Invalid file type. Please upload a supported file.',
        limitReached: 'Compression limit reached. Please login for unlimited access.',
        loginSuccess: 'Successfully logged in!',
        loginFailed: 'Login failed. Please try again.',
        logoutSuccess: 'Successfully logged out!',
        logoutFailed: 'Logout failed, please try again.',
        online: 'You are back online!',
        offline: 'You are offline. Some features may not work.',
        noFileSelected: 'No file selected. Please choose a file to process.',
        errorProcessingFile: 'An error occurred during file processing.',
        
        // New compression options
        compressionMethod: 'Compression Method:',
        aiSelection: 'AI Selection (Automatic)',
        gzipCompression: 'Gzip Compression',
        brotliCompression: 'Brotli Compression',
        webpOptimization: 'WebP Optimization',
        pdfOptimization: 'PDF Optimization',
        officeOptimization: 'Office Optimization',
        videoOptimization: 'Video Optimization',
        compressionProfile: 'Compression Profile:',
        defaultProfile: 'Default',
        webProfile: 'Web',
        archiveProfile: 'Archive',
        networkProfile: 'Network',
        sensitiveMode: 'Sensitive Mode (Detect sensitive content)',
        processFile: 'Process File',
        fileSelected: "File Selected",
        readyToCompress: "Ready to compress",
        changeFile: "Change File",
        
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
        backendTitle: 'Backend',
        delete: 'Delete',
        historyEntryDeleted: 'History entry deleted successfully.',
        
        // Compression methods descriptions
        aiDescription: 'Automatically selects the best compression method based on file type and content',
        gzipDescription: 'Standard compression algorithm, good for general files',
        brotliDescription: 'Modern compression algorithm, excellent for web content',
        webpDescription: 'Optimizes images to WebP format for better compression',
        pdfDescription: 'Optimizes PDF files by removing unnecessary metadata',
        officeDescription: 'Optimizes Microsoft Office documents',
        videoDescription: 'Optimizes video files for smaller size'
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
        method: 'Metode',
        action: 'Aksi',
        download: 'Unduh',
        compare: 'Bandingkan',
        delete: 'Hapus',
        login: 'Masuk',
        logout: 'Keluar',
        home: 'Beranda',
        about: 'Tentang',
        compressing: 'Mengompres',
        compressionSuccess: 'File berhasil dikompres!',
        compressionFailed: 'Kompresi gagal. Silakan coba lagi.',
        downloadFailed: 'Unduhan gagal. Silakan coba lagi.',
        invalidFileType: 'Tipe file tidak valid. Silakan unggah file yang didukung.',
        limitReached: 'Batas kompresi tercapai. Silakan masuk untuk akses tak terbatas.',
        loginSuccess: 'Berhasil masuk!',
        loginFailed: 'Gagal masuk. Silakan coba lagi.',
        logoutSuccess: 'Berhasil keluar!',
        logoutFailed: 'Gagal keluar. Silakan coba lagi.',
        online: 'Anda kembali online!',
        offline: 'Anda sedang offline. Beberapa fitur mungkin tidak berfungsi.',
        noFileSelected: 'Tidak ada file yang dipilih. Harap pilih file untuk diproses.',
        errorProcessingFile: 'Terjadi kesalahan selama pemrosesan file.',
        
        // New compression options (Bahasa Indonesia)
        compressionMethod: 'Metode Kompresi:',
        aiSelection: 'Pemilihan AI (Otomatis)',
        gzipCompression: 'Kompresi Gzip',
        brotliCompression: 'Kompresi Brotli',
        webpOptimization: 'Optimasi WebP',
        pdfOptimization: 'Optimasi PDF',
        officeOptimization: 'Optimasi Office',
        videoOptimization: 'Optimasi Video',
        compressionProfile: 'Profil Kompresi:',
        defaultProfile: 'Default',
        webProfile: 'Web',
        archiveProfile: 'Arsip',
        networkProfile: 'Jaringan',
        sensitiveMode: 'Mode Sensitif (Deteksi konten sensitif)',
        processFile: 'Proses File',
        fileSelected: "File Terpilih",
        readyToCompress: "Siap untuk dikompresi",
        changeFile: "Ganti File",
        
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
        techStackTitle: 'Technology Stack',
        frontendTitle: 'Frontend',
        backendTitle: 'Backend',
        technologyUsedTitle: 'Teknologi yang Digunakan',
        
        // How to Use Page Translations
        howToUseTitle: 'Cara Menggunakan Compressio',
        step1: 'Unggah File Anda: Seret dan lepaskan file Anda ke area yang ditentukan atau klik "Pilih File" untuk memilihnya dari perangkat Anda.',
        step2: 'Pilih Jenis Kompresi: Pilih antara "Kompres" atau "Dekompresi" berdasarkan kebutuhan Anda.',
        step3: 'Pilih Algoritma (Opsional): Pilih algoritma kompresi pilihan Anda. Otomatis (secara otomatis memilih algoritma terbaik untuk file Anda), Huffman Coding (metode efisien untuk kompresi data lossless), atau Run-Length Encoding (bentuk kompresi data di mana urutan data disimpan sebagai nilai data tunggal dan hitungan).',
        step4: 'Proses File: Klik tombol "Proses File" untuk memulai kompresi atau dekompresi.',
        step5: 'Unduh Hasil: Setelah diproses, file yang dikompres/didekompres akan muncul di tabel "Kompresi Terbaru". Klik "Unduh" untuk menyimpannya.',
        delete: 'Hapus',
        historyEntryDeleted: 'Entri riwayat berhasil dihapus.',
        
        // Compression methods descriptions (Bahasa Indonesia)
        aiDescription: 'Secara otomatis memilih metode kompresi terbaik berdasarkan jenis file dan konten',
        gzipDescription: 'Algoritma kompresi standar, bagus untuk file umum',
        brotliDescription: 'Algoritma kompresi modern, sangat baik untuk konten web',
        webpDescription: 'Mengoptimalkan gambar ke format WebP untuk kompresi yang lebih baik',
        pdfDescription: 'Mengoptimalkan file PDF dengan menghapus metadata yang tidak perlu',
        officeDescription: 'Mengoptimalkan dokumen Microsoft Office',
        videoDescription: 'Mengoptimalkan file video untuk ukuran yang lebih kecil'
    }
};

// Placeholder for compression limit check (moved from compress.js)
function checkCompressionLimit() {
    // For now, always allow compression. 
    // This function will be properly implemented with authentication logic.
    return true;
}

// Declare fileCompressor globally, but initialize it inside initializeApp
let fileCompressor;

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
const API_BASE_URL = 'http://localhost:8000'; // Diperbarui untuk menunjuk ke backend lokal FastAPI

// State management
let compressionHistory = JSON.parse(localStorage.getItem('compressionHistory') || '[]');

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const compressionType = document.getElementById('compressionType'); // Mungkin tidak diperlukan lagi jika seleksi AI penuh di backend
const historyTable = document.getElementById('historyTable');
const selectedFileNameDisplay = document.getElementById('selectedFileName'); // Tampilan nama file yang dipilih
const fileNameSpan = document.getElementById('fileNameDisplay'); // Span untuk nama file
const clearFileBtn = document.getElementById('clearFileSelection'); // Tombol untuk menghapus pilihan file
const processFileButton = document.querySelector('#uploadForm button[type="submit"]'); // Tombol proses file

// Event Listeners
const dropZone = document.getElementById('dropZone');

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Initialize file compressor here to ensure compress.js has loaded
    window.fileCompressor = new FileCompressor(checkCompressionLimit); // Paparkan secara global untuk akses yang lebih mudah

    // Set up file input change handler
    fileInput.addEventListener('change', handleFileSelect);
    
    // Set up form submit handler - Delegasikan ke fileCompressor.compressFile
    uploadForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Mencegah pengiriman form default
        const files = fileInput.files; // Ambil file dari input
        if (files.length > 0) {
            window.fileCompressor.compressFile(files[0]); // Panggil metode kompresi
        } else {
            showToast(translations[getCurrentLanguage()].noFileSelected, 'warning');
        }
    });

    // Set up clear file selection button
    if (clearFileBtn) {
        clearFileBtn.addEventListener('click', clearFileSelection);
    }

    // Update UI language on load
    updateLanguage(getCurrentLanguage());

    // Populate compression history on load
    window.fileCompressor.loadCompressionHistory();
}

// Handle file selection from input
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displaySelectedFile(file.name);
        // `fileCompressor.handleFiles` akan dipanggil pada `form submit` atau `drop`
        // Jadi, hanya perlu menampilkan nama file yang dipilih di sini.
    } else {
        clearFileSelection();
    }
}

// Fungsi handleFormSubmit sebelumnya kini di-inline ke event listener submit di initializeApp
// Fungsi showCompressionProgress, updateCompressionProgress, removeCompressionProgress, showCompressionResults
// kini ditangani atau tidak relevan lagi karena logika utama di compress.js

function displaySelectedFile(fileName) {
    if (selectedFileNameDisplay) {
        selectedFileNameDisplay.textContent = fileName;
        selectedFileNameDisplay.style.display = 'block';
    }
    if (fileNameSpan) {
        fileNameSpan.textContent = fileName;
        fileNameSpan.style.display = 'inline';
    }
    if (clearFileBtn) {
        clearFileBtn.style.display = 'inline-block';
    }
    if (processFileButton) {
        processFileButton.disabled = false;
    }
    // Update dropZone innerHTML based on selected file
    const dropZone = document.getElementById('dropZone');
    if (dropZone) {
        dropZone.innerHTML = `
            <h3>${translations[getCurrentLanguage()].fileSelected}: ${fileName}</h3>
            <p>${translations[getCurrentLanguage()].readyToCompress}</p>
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                ${translations[getCurrentLanguage()].changeFile}
            </button>
        `;
        // Reattach event listener to the newly created fileInput element
        document.getElementById('fileInput').addEventListener('change', handleFileSelect);
    }
}

function clearFileSelection() {
    fileInput.value = ''; // Clear the selected file from the input
    if (selectedFileNameDisplay) {
        selectedFileNameDisplay.textContent = '';
        selectedFileNameDisplay.style.display = 'none';
    }
    if (fileNameSpan) {
    fileNameSpan.textContent = '';
        fileNameSpan.style.display = 'none';
    }
    if (clearFileBtn) {
        clearFileBtn.style.display = 'none';
    }
    if (processFileButton) {
        processFileButton.disabled = true;
    }
    // Restore dropZone innerHTML to initial state
    const dropZone = document.getElementById('dropZone');
    if (dropZone) {
        dropZone.innerHTML = `
            <h3>${translations[getCurrentLanguage()].dragDrop}</h3>
            <p>${translations[getCurrentLanguage()].or}</p>
            <input type="file" id="fileInput" class="d-none" accept=".jpg,.jpeg,.png,.txt,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.mp4,.mpeg,.mov,.mp3,.wav,.json,.bin">
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                ${translations[getCurrentLanguage()].chooseFiles}
            </button>
        `;
        // Reattach event listener to the newly created fileInput element
        document.getElementById('fileInput').addEventListener('change', handleFileSelect);
    }
}

// These functions are now handled by FileCompressor in compress.js or are no longer needed here.
// Keeping them for context, but they will be removed if no longer referenced.
function validateCompressionSettings(file, compressionType, operation) {
    // Logic is now primarily in isValidFile in compress.js
    return true;
}

const COMPRESSION_TYPES = {
    AUTO: 'auto',
    HUFFMAN: 'huffman',
    RLE: 'rle'
};

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