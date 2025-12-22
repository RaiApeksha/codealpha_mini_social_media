function loadPosts() {
    fetch('/api/posts/')
    .then(res => res.json())
    .then(data => {
        let postsDiv = document.getElementById('posts');
        postsDiv.innerHTML = '';

        data.posts.forEach(post => {
            let commentsHtml = '';
            post.comments.forEach(c => {
                commentsHtml += `<p><b>${c.user}</b>: ${c.text}</p>`;
            });

            postsDiv.innerHTML += `
                <div class="post">
                    <b>${post.user}</b>
                    <p>${post.content}</p>

                    <button onclick="likePost(${post.id})">
                        ❤️ ${post.likes}
                    </button>

                    <div class="comments">
                        ${commentsHtml}
                        <input type="text" id="comment-${post.id}" placeholder="Write a comment..." />
                        <button onclick="addComment(${post.id})">Comment</button>
                    </div>
                </div>
                <hr>
            `;
        });
    });
}


function createPost() {
    let content = document.getElementById('postContent').value;

    fetch('/api/posts/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content })
    })
    .then(() => {
        document.getElementById('postContent').value = '';
        loadPosts();
    });
}

function likePost(postId) {
    fetch('/api/posts/like/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postId })
    })
    .then(res => res.json())
    .then(() => loadPosts());
}

loadPosts();
function addComment(postId) {
    let text = document.getElementById(`comment-${postId}`).value;

    fetch('/api/comments/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            post_id: postId,
            text: text
        })
    })
    .then(() => loadPosts());
}
