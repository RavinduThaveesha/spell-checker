$(document).ready(function(){

    var config = {
        'strawbery':['strawberry'],
        'bluebery': ['blueberry'],
        'banananana':[]
    };

    var text = $('[contenteditable]').text();
    $('#textarea').html(updateText(config, text));

    //send text to server through API
    $('#submit').on('click', function(e){
        //if (e.keyCode === 13) {
            text = $('#textarea').text();
            $.ajax({
                url: "http://127.0.0.1:8000/api/check/",
                data: {
                    'text': text
                },
                method: 'POST',
                success: function(result){
                    config = result
                    $('#textarea').html(updateText(config, text));
                }
            });
        //}
    });

    $("#text-count-lbl span").html(text.split(' ').length);

    $(document).on('click', '.suggestions-yes ul li', function(){
        if ($(this).text() == 'ignore') {
            let span = $(this).closest('.suggestions-yes');
            span.replaceWith($(this).attr('data-word'));
        } else {
            $(this).closest('.suggestions-yes').replaceWith($(this).text());
        }

        $("#text-count-lbl span").html($('#textarea').text().length);
    });

    $(document).on('click', '.suggestions-no ul li', function(){
        $(this).closest('.suggestions-no').replaceWith($(this).attr('data-word'));
        $("#text-count-lbl span").html($('#textarea').text().length);
    });

    $(document).on('click', '.suggestions-yes', function(){
        let items = config[$(this).attr('id')];
        let ul = $('<ul/>');
        $.each(items, function (index, value) {
            ul.append($('<li/>').html(value));
         });
        ul.append($('<li class="ignore" data-word="'+ $(this).attr('id') +'"/>').html('ignore'));
        $(this).append(ul);
    });

    $(document).on('click', '.suggestions-no', function(){
        let ul = $('<ul/>');
        ul.append($('<li class="ignore" data-word="'+ $(this).attr('id') +'"/>').html('no suggestions'));
        $(this).append(ul);
    });


    $('#textarea').on('input blur keydown keyup', function(){
        $("#text-count-lbl span").html($(this).text().split(' ').length);
        // if($('.suggestions-yes ul').length) {
        //     $('.suggestions-yes ul').remove()
        // }

        // if($('.suggestions-no ul').length) {
        //     $('.suggestions-no ul').remove()
        // }
    });


     $.ajax({
        url: "http://127.0.0.1:8000/api/dictionary",
        method: 'GET',
        success: function(result) {
            let dict = $('#dictionary').val(result)
            $.each(result, function(key, value) {
                dict.append('<option value="">' + key + '</option>');
            })
        }
    });

    $('#dictionary').select2({
         theme: "classic"
    });

});

function updateText(config, text) {
    for (let key in config) {
        let cls = 'suggestions-yes';
        let regEx = new RegExp("\\b" + key + "\\b", 'i');

        // if(config[key].length) {
        //     cls = 'suggestions-yes';
        // }

        text = text.replace(regEx, `<span class="${cls}" id="${key}">${key}</span>`);
    }

    return text;
}
