function subject_search(){
    var $select = $('#id_subject').selectize({
        valueField: 'title',
        labelField: 'title',
        searchField: 'title',
        placeholder: 'Поиск предмета ...',
        options: [],
        create: true,
        multiple: false,
        load: function(query, callback) {
            if (!query  || query.length < 2) return callback();
            $.ajax({
                url: '/directory/subject/search',
                type: 'GET',
                data: {
                    q: query
                },
                error: function() {
                    callback();
                },
                success: function(res) {
                    return callback(res);
                }
            })
        }
    })
}


var $modal = $('#universal-modal')
$(document).on('click','.open-universal-modal',function(){
    var $link = $(this);
    var url = $link.data('modal-url')
    var title = $link.data('modal-title')
    if (url && title) {
        event.preventDefault();
        $('.modal-title', $modal).text(title);
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $('#universal-modal-content').html(data)
                $modal.on('shown.bs.modal', function () {
                }).modal('show');
                subject_search()
            }
        })
    }
});

$(document).on('submit','#form-universal-modal',function(){
    event.preventDefault()
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: new FormData(this),
        dataType: 'json',
        contentType: false,
        cache: false,
        processData:false,
        success: function(response) {
          if(!response.success){
            $('#form-universal-modal-content').html(response.form_html)
          }
          else{
            redirect_url = response.redirect_url
            if(redirect_url){
                location.href = redirect_url
            }
          }
        },
        error: function (response) {
            alert('error....')
        }
    });
})

$(document).on('submit','#form-universal-multipart-modal',function(){
    event.preventDefault()
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        success: function(response) {
          if(!response.success){
            $('#form-universal-modal-content').html(response.form_html)
          }
          else{
            redirect_url = response.redirect_url
            if(redirect_url){
                location.href = redirect_url
            }
          }
        },
        error: function (response) {
            alert('error....')
        }
    });
})


$(document).on('submit','#form-register-modal',function(){
    event.preventDefault()
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: new FormData(this),
        dataType: 'json',
        contentType: false,
        cache: false,
        processData:false,
        beforeSend: function(){
        },
        success: function(response) {
          if(!response.success){
            $('#form-demand-content').html(response.form_html)
            $('#form-register-content').html(response.register_form_html)
          }
          else{
            redirect_url = response.redirect_url
            if(redirect_url){
                location.href = redirect_url
            }
          }
        },
        error: function (response) {
        }
    });
})

$(document).on('change','.type-selected',function(){
    alert('test....')
}