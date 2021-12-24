let upload = () =>
{

    let timerInterval
    Swal.fire({
      title: 'Traitement en cours...!',
      html: '',
      timer: 2600,
      showCloseButton: true,
      timerProgressBar: true,
      didOpen: () => {
       
        
        const b = Swal.getHtmlContainer().querySelector('b')
        timerInterval = setInterval(() => {
          b.textContent = Swal.getTimerLeft()
        }, 100)
      },
      willClose: () => {
        clearInterval(timerInterval)
      }
    }).then((result) => {
      /* Read more about handling dismissals below */
      if (result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer')
      }
    })
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
        update_table(response.data)
    }).catch(function (error) {
        console.log(error);
    });
}


let update_table = (data) =>
{
    console.log("data" ,data)
    var myTable = $('#myTable').DataTable();
    myTable.clear().draw();
    data.map(
        elem =>
        {
            myTable.row.add(
            [
                '<img  src=' +elem.image + ' alt="" width="300" height="200">',
                elem.score,
                '<div><form action""><input type ="submit" value="Positive"/></form><button class ="k-state-selected">Nigative</button></div>'
            ]
            ).draw();
           // alert(elem.image)

            $('.k-state-selected').on("click", function(){
               var p=elem.image;
               
             alert(p);
             });
        }
    )
}


