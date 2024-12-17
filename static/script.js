// Function to handle following/unfollowing an author
function followAuthor(button, reload = null) { 
  const author = button.dataset.author; // Retrieve author's identifier
  const following = (button.dataset.following?.toLowerCase?.() === 'true'); // Check current follow state

  fetch(`/follow/${author}`, {
    method: 'POST', // Send a POST request to toggle follow status
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      now_following: !following, // Toggle the follow state
    }),
  })
  .then(response => {
    if (!response.ok) { // Check if the server responded correctly
      throw new Error(`Server error: ${response.status}`);
    }
    return response.json(); // Parse JSON response
  })
  .then(response => {
    if (response.now_following !== undefined) { // Ensure the server returned valid data
      const followButtons = document.getElementsByClassName('follow_button');
      for (let i = 0; i < followButtons.length; i++) {
        if (followButtons[i].dataset.author === author) {
          const followButton = followButtons[i];
          // Update button text and data based on follow status
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
        location.reload(); // Reload the page if needed
      }
    } else {
      console.error('Invalid response format:', response); // Log an error if response is invalid
    }
  })
  .catch(error => {
    console.error('Error:', error); // Handle any errors
    alert('Failed to toggle follow status. Please try again.');
  });
}

// Function to handle rating a post (like/dislike)
  function ratePost(button) {
    const selected = (button.dataset.selected?.toLowerCase?.() === 'true'); // Is this button already selected?
    const value = button.dataset.value; // Rating value
    const id = button.dataset.id; // Post ID
    const desire = selected ? 0 : value; // Toggle selection state

    fetch(`/posts/${id}/rating/${desire}`, { method: 'POST' })
    .then(response => response.json())
    .then(response => {
      const newRating = response.rating; // New rating returned by server
      const up = button.parentNode.children[0]; // Upvote button
      const down = button.parentNode.children[1]; // Downvote button
      let oldRating = 0;

      // Determine the previous state of the buttons
      if (up.dataset.selected?.toLowerCase?.() === 'true') {
        oldRating = 1;
      } else if (down.dataset.selected?.toLowerCase?.() === 'true') {
        oldRating = 2;
      }

    // Reset button states
    up.classList.remove('highlight');
    down.classList.remove('highlight');
    up.dataset.selected = down.dataset.selected = false;

    // Update the vote counts and highlights based on new rating
    if (newRating === 0) {
      if (oldRating === 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
      } else if (oldRating === 2) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    }

    if (newRating === 1) { // Upvoted
      up.classList.add('highlight');
      up.dataset.selected = true;
      if (oldRating === 0) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
      } else if (oldRating === 2) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    } else if (newRating === 2) { // Downvoted
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

// Function to handle rating a comment (like/dislike)
  function rateComment(button) {
    const selected = (button.dataset.selected?.toLowerCase?.() === 'true'); // Is this button already selected?
    const value = button.dataset.value; // Rating value
    const id = button.dataset.id; // Comment ID
    const desire = selected ? 0 : value; // Toggle selection state

    fetch(`/comments/${id}/rating/${desire}`, { method: 'POST' })
    .then(response => response.json())
    .then(response => {
      const newRating = response.rating; // New rating returned by server
      const up = button.parentNode.children[0]; // Upvote button
      const down = button.parentNode.children[1]; // Downvote button
      let oldRating = 0;

      // Determine the previous state of the buttons
      if (up.dataset.selected?.toLowerCase?.() === 'true') {
        oldRating = 1;
      } else if (down.dataset.selected?.toLowerCase?.() === 'true') {
        oldRating = 2;
      }

      // Reset button states
      up.classList.remove('highlight');
      down.classList.remove('highlight');
      up.dataset.selected = down.dataset.selected = false;

      // Update the vote counts and highlights based on new rating
      if (newRating === 0) {
        if (oldRating === 1) {
          up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
        } else if (oldRating === 2) {
          down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
        }
      }

      if (newRating === 1) { // Upvoted
        up.classList.add('highlight');
        up.dataset.selected = true;
        if (oldRating === 0) {
          up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        } else if (oldRating === 2) {
          up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
          down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
        }
      } else if (newRating === 2) { // Downvoted
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
