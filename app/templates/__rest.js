document.addEventListener('DOMContentLoaded', function () {
  document.querySelector(".btn-primary").onclick = function () {
    const post = document.createElement('input');
    const bttn = document.createElement('button');
    post.placeholder = 'add your text here';
    bttn.id = "submit_it";
    bttn.innerHTML = "Submit";
    document.querySelector('#insert_row').appendChild(post);
    document.querySelector('#insert_row').appendChild(bttn);
    document.querySelector('#submit_it').onclick = function () {
      if (post.value == '') {
        alert('You cannot post empty form!');
      }
      else {
        const request = new XMLHttpRequest();
        const postext = post.value;
        request.open('POST', '/addpost');
        const data = new FormData();
        data.append('postext', postext);
        request.send(data);
        return false;
      }
    }
  }
});
