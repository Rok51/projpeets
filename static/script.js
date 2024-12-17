function followAuthor(button, reload = null) { 
  const author = button.dataset.author;
  const following = (button.dataset.following?.toLowerCase?.() === 'true');

  fetch(`/follow/${author}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      now_following: !following, // Now following/ Not following
    }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    return response.json();
  })
  .then(response => {
    if (response.now_following !== undefined) { // Make sure the server is valid
      const followButtons = document.getElementsByClassName('follow_button');
      for (let i = 0; i < followButtons.length; i++) {
        if (followButtons[i].dataset.author === author) {
          const followButton = followButtons[i];
          if (response.now_following) {
            followButton.innerHTML = 'Following';
            followButton.dataset.following = 'true';
          } else {
            followButton.innerHTML = 'Follow';
            followButton.dataset.following = 'false';
          }
        }
      }
      if (reload) { 
        location.reload(); // Reload if reload flag passes
      }
    } else {
      console.error('Invalid response format:', response);
    }
  })
  .catch(error => {
    console.error('Error:', error); // Log Errors
    alert('Failed to toggle follow status. Please try again.');
  });
}


function ratePost(button) {
  const selected = (button.dataset.selected?.toLowerCase?.() === 'true');
  const value = button.dataset.value;
  const id = button.dataset.id;
  const desire = selected ? 0 : value;

  fetch(`/posts/${id}/rating/${desire}`, {
    method: 'POST',
  }).then(response => response.json()).then(response => {
    const newRating = response.rating;
    const up = button.parentNode.children[0];
    const down = button.parentNode.children[1];
    let oldRating = 0;

    if (up.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 1;
    } else if (down.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 2;
    }

    up.classList.remove('highlight');
    down.classList.remove('highlight');
    up.dataset.selected = down.dataset.selected = false;

    if (newRating === 0) {
      if (oldRating === 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
      } else if (oldRating === 2) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    }

    if (newRating === 1) {
      up.classList.add('highlight');
      up.dataset.selected = true;
      if (oldRating === 0) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
      } else if (oldRating === 2) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    } else if (newRating === 2) {
      down.classList.add('highlight');
      down.dataset.selected = true;
      if (oldRating === 0) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      } else if (oldRating === 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      }
    }
  });
}

function rateComment(button) {
  const selected = (button.dataset.selected?.toLowerCase?.() === 'true');
  const value = button.dataset.value;
  const id = button.dataset.id;
  const desire = selected ? 0 : value;

  fetch(`/comments/${id}/rating/${desire}`, {
    method: 'POST',
  }).then(response => response.json()).then(response => {
    const newRating = response.rating;
    const up = button.parentNode.children[0];
    const down = button.parentNode.children[1];
    let oldRating = 0;

    if (up.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 1;
    } else if (down.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 2;
    }

    up.classList.remove('highlight');
    down.classList.remove('highlight');
    up.dataset.selected = down.dataset.selected = false;

    if (newRating === 0) {
      if (oldRating === 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
      } else if (oldRating === 2) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    }

    if (newRating === 1) {
      up.classList.add('highlight');
      up.dataset.selected = true;
      if (oldRating === 0) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
      } else if (oldRating === 2) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    } else if (newRating === 2) {
      down.classList.add('highlight');
      down.dataset.selected = true;
      if (oldRating === 0) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      } else if (oldRating === 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      }
    }
  });
}
