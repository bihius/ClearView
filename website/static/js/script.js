document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();
        const photos = document.querySelectorAll('li');
        photos.forEach(function(photo) {
            const description = photo.querySelector('p').textContent.toLowerCase();
            if (description.includes(searchTerm)) {
                photo.style.display = '';
            } else {
                photo.style.display = 'none';
            }
        });
    });
});
