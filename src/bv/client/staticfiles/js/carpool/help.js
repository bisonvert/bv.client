for (i = 1; i <= 6; i++) {
    $('help_dt_img_'+i).observe('click', function(event) {
        var element = event.element();
        var regex = new RegExp("^help_dt_img_([0-9]+)$");
        var match = regex.exec(element.id);
        if (match !== null) {
            key = match[1];
            $('help_dd_'+key).toggle();
            element.setAttribute('src', media_url+'img/'+($('help_dd_'+key).visible() ? 'hide' : 'show')+'.png');
        }
    });
}
