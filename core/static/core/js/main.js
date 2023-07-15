document.getElementById("load-dir").addEventListener("click", function(event){
    event.preventDefault();
    fetch('get_directories/')
        .then(response => response.text())
        .then(data => {
            document.getElementById('dir-list').innerHTML = data;
        });
});
