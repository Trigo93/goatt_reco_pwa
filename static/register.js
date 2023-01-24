if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/static/sw.js', {scope: '/static/'}).then(function(registration) {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
        console.log('ServiceWorker registration failed: ', err);
    });
  });
}
