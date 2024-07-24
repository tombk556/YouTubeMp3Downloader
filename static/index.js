const form = document.querySelector('#download-form');
form.addEventListener('submit', (event) => {
  const urlInput = document.querySelector('#url');
  const titleInput = document.querySelector('#title');
  const artistInput = document.querySelector('#artist');
  if (!urlInput.value.startsWith('https://www.youtube.com/watch') || !titleInput.value || !artistInput.value) {
    event.preventDefault();
    alert('Please enter a valid YouTube URL, title, and artist.');
  }
});