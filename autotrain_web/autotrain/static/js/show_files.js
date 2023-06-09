    var photoContainer = document.getElementById('photo-container');
    var photoItems = Array.from(photoContainer.getElementsByClassName('photo-item'));
    var currentIndex = 0;

    function showPhoto(index) {
      photoItems.forEach(function(item, i) {
        if (i === index) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    }

    function nextPhoto() {
      currentIndex = (currentIndex + 1) % photoItems.length;
      showPhoto(currentIndex);
    }

    function prevPhoto() {
      currentIndex = (currentIndex - 1 + photoItems.length) % photoItems.length;
      showPhoto(currentIndex);
    }

    document.getElementById('prev-button').addEventListener('click', prevPhoto);
    document.getElementById('next-button').addEventListener('click', nextPhoto);

    showPhoto(currentIndex);