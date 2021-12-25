let upload = () =>
{

    let formData = new FormData();
    let img = document.getElementById('img').files[0]

    if(img == null)
    {
      Swal.fire({
        timer: 2600,
        icon: 'error',
        title: 'Oops...',
        text: 'Veuillez choisir une image',
        showCloseButton: true,})
        return -1
    }

    formData.append("image", img);
    axios.post('upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
    }
    }).then(function (response) {
        update_result(response.data)
    }).catch(function (error) {
        console.log(error);
    });
}



let update_result = (data) =>
 {
  console.log("data" ,data) 
  var div = document.getElementById('mydiv'); 
data.map(
  elem =>
  { 

    div.innerHTML +='<a href=' +elem.image+ ' target="_blank" > <img src='+ elem.image + '  style="width:300px; height:300px"/>';  
  }
) 
 
 }



