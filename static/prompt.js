window.addEventListener('beforeinstallprompt', (e) => {
    // Stash the event so it can be triggered later.
    deferredPrompt = e;
    showAddToHomeScreenPrompt();
});

function showAddToHomeScreenPrompt() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
            } else {
                console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
        });
    }
}
