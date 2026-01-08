console.log("MAIN JS LOADED ✅");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function likePost(postId) {
    fetch(`/api/like/${postId}/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(res => res.json())
    .then(data => {
        const likesSpan = document.getElementById(`likes-${postId}`);
        if (likesSpan) {
            likesSpan.innerText = data.likes;
        }
    })
    .catch(err => console.error('Like error:', err));
}

function addComment(postId) {
    const input = document.getElementById(`comment-${postId}`);
    const text = input.value.trim();

    if (!text) return;

    fetch(`/api/comment/${postId}/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(() => {
        input.value = '';
        location.reload(); // simple + reliable
    })
    .catch(err => console.error('Comment error:', err));
}
