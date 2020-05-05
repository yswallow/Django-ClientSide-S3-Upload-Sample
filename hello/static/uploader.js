window.onload = function() {
    document.getElementById("file_input").onchange = function(){
        var files = document.getElementById("file_input").files;
        var file = files[0];
        if(!file){
            return alert("No file selected.");
        }
        getSignedRequest(file);
    };
};

function getSignedRequest(file){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                uploadFile(file, response.data, response.key);
            }
            else{
                alert("Could not get signed URL.");
            }
        }
    };
    xhr.send();
}  

function changeImage(s3key) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_image_url?file_name="+s3key);
  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4) {
      if(xhr.status === 200) {
        url = xhr.response
        document.getElementById("preview").src = url;
        document.getElementById("avatar-url").value = s3key;
      } else {
        alert("Could not get image url");
      }
    }
  }
  xhr.send();
}

function uploadFile(file, s3Data, s3key){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url);

  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.open("POST", s3Data.url);
  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        changeImage(s3key);
      }
      else{
        alert("Could not upload file.");
      }
   }
  };
  xhr.send(postData);
}
