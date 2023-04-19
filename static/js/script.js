window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

///////////////////////////////////////////////////////////
 /* function load_data(specialities){
    $.ajax({
      url: "/doctors",
      type: "POST",
      data:{specialities:specialities},
      success:function(response) {
        alert(specialities);
        var data = response;
        var data_html = '';
        $.each(data, function(index, value) {
            data_html += '<li>' + value + '</li>';
        });
        $('#doctors').html(data_html);
      },
    })
  }
  $('#specialities').change(function(){
    var specialities = $("#specialities option:selected" ).text(); //$(this).val();
    load_data(specialities);
    
    });*/





   /* $(document).ready(function() {
        $('.delete-btn').click(function() {
          const buttonElement = document.querySelector('.delete-btn');
          const doctor_id = buttonElement.getAttribute('data-id');
          //alert(doctor_id);
          /*fetch('/doctors/' + doctor_id, {
            method: 'DELETE'
          })
          .then(function() {
            const item = e.target.parentElement;
            item.remove();
          })
          fetch('/doctors/' + doctor_id, {
              method: 'DELETE'
            })
            .then(response => {
              if (response.ok) {
                console.log('Doctor deleted successfully');
              } else {
                console.log('Error deleting doctor');
              }
            })
            .catch(error => {
              console.error('Error deleting doctor:', error);
            });

        });
    })*/
