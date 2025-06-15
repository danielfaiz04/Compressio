// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAgb2EzmCQ5kHE9TxAAnk7m4FSGbsDsGFE",
    authDomain: "compressio-78a31.firebaseapp.com",
    projectId: "compressio-78a31",
    storageBucket: "compressio-78a31.appspot.com",
    messagingSenderId: "105545599922149657425",
    appId: "1:569817073799:web:59c82b7a2cdc8fb8cfd022"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

// Auth state observer
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User is signed in
        document.getElementById('loginBtn').textContent = 'Sign Out';
        document.getElementById('loginBtn').classList.remove('btn-outline-primary');
        document.getElementById('loginBtn').classList.add('btn-primary');
        
        // Store user info in localStorage
        localStorage.setItem('user', JSON.stringify({
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL
        }));
        
        // Update UI for authenticated user
        updateUIForAuthenticatedUser();
    } else {
        // User is signed out
        document.getElementById('loginBtn').textContent = 'Sign in with Google';
        document.getElementById('loginBtn').classList.remove('btn-primary');
        document.getElementById('loginBtn').classList.add('btn-outline-primary');
        
        // Clear user info from localStorage
        localStorage.removeItem('user');
        
        // Update UI for non-authenticated user
        updateUIForNonAuthenticatedUser();
    }
});

// Sign in with Google
function signInWithGoogle() {
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider)
        .then((result) => {
            // The signed-in user info.
            const user = result.user;
            // This gives you a Google Access Token. You can use it to access the Google API.
            const credential = result.credential;
            
            // Check if it's a new user
            const isNewUser = result.additionalUserInfo.isNewUser;

            if (isNewUser) {
                showToast(translations[localStorage.getItem('preferredLanguage') || 'id'].loginSuccessNewUser, 'success');
                // You can add additional registration steps here if needed, e.g., prompt for more profile info
            } else {
                showToast(translations[localStorage.getItem('preferredLanguage') || 'id'].loginSuccess, 'success');
            }
        })
        .catch((error) => {
            console.error('Error signing in with Google:', error);
            showToast('Error signing in with Google', 'error');
        });
}

// Sign out
function signOut() {
    firebase.auth().signOut()
        .catch((error) => {
            console.error('Error signing out:', error);
            showToast('Error signing out', 'error');
        });
}

// Update UI for authenticated user
function updateUIForAuthenticatedUser() {
    // Remove compression limit
    localStorage.removeItem('compressionCount');
    
    // Update history section
    const historySection = document.querySelector('.compression-history');
    if (historySection) {
        historySection.classList.remove('limited');
    }
}

// Update UI for non-authenticated user
function updateUIForNonAuthenticatedUser() {
    // Initialize compression count if not exists
    if (!localStorage.getItem('compressionCount')) {
        localStorage.setItem('compressionCount', '0');
    }
    
    // Update history section
    const historySection = document.querySelector('.compression-history');
    if (historySection) {
        historySection.classList.add('limited');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast fade-in ${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    const toastContainer = document.querySelector('.toast-container');
    if (toastContainer) {
        toastContainer.appendChild(toast);
    } else {
        document.body.appendChild(toast);
    }

    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const googleSignInBtn = document.getElementById('googleSignIn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            const user = JSON.parse(localStorage.getItem('user'));
            if (user) {
                signOut();
            } else {
                const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
                loginModal.show();
            }
        });
    }
    
    if (googleSignInBtn) {
        googleSignInBtn.addEventListener('click', signInWithGoogle);
    }
}); 