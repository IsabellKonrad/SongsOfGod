send_message = function(message){
    var m = $('<div />').addClass("modal fade").attr("data-role","dialog");
    var dialog = $('<div />').addClass("modal-dialog");
    var content = $('<div />').addClass("modal-content");
    var body = $('<div />').addClass("modal-body");
    var mtext = $('<p />').text(message);
    var btn_close = $('<button />').addClass("btn btn-default").attr("data-dismiss","modal").text("Close");
    body.append(mtext);
    body.append(btn_close);
    content.append(body);
    dialog.append(content);
    m.append(dialog);
    m.modal();
}


change_select_song = function(){
    $("#show_pdf_check").remove();
    $("#btn_save_song").addClass("hidden");
    $("#btn_check_song").addClass("hidden");
}


make_song_selector = function(){
  var div = $('<div />').addClass("placeholder_selectgroup");

  var select_song = $('<select />').attr("id","select_song").addClass("class_selected_songs")
      .css("width", "55%").on("change",function (){change_select_song();});
  div.append(select_song);
  $(select_song).select2({placeholder: "Lied"});

  var span_space = $('<span />').css("margin-left","5px").css("margin-right","5px");
  div.append(span_space);

  songlist.forEach(function(element){
    var option = $('<option />').text(element[1]).val(element[0]);
    select_song.append(option);
  });

  var btn_get_lyrics = $('<button />').addClass("btn btn-info").text("Get lyrics")
    .css("margin-left","5px").on("click", function() {get_lyrics();});
  div.append(btn_get_lyrics);
  return div;
};


get_lyrics = function(){
    var selected_song = $("#select_song").find(":selected").val();
    var data = {"selected_song": selected_song};
    $.ajax({
      contentType: 'application/json',
      type: 'POST',
      url: 'getsongedit',
      data: JSON.stringify(data),
      success: function(d){
        send_message("Der Quellcode des Liedes ist in Latex geschrieben. Bitte ändere nicht die Textstruktur.");
        $("#btn_check_song").removeClass("hidden");
        $("#btn_save_song").addClass("hidden");
        $("#show_pdf_check").remove();
        $("#show_lyrics_placeholder").val(d.lyrics);
      },
      error: function(obj, st, err){
        alert(err);
      }
    });
}

check_song = function(){
    $("#show_pdf_check").remove();
    var songcontent = $("#show_lyrics_placeholder").val();
    var data = {"songcontent": songcontent};
    $.ajax({
      contentType: 'application/json',
      type: 'POST',
      url: 'checksongedit',
      data: JSON.stringify(data),
      success: function(d){
        $("#show_pdf_check_placeholder").append(d.pdfpath);
        $("#btn_save_song").removeClass("hidden");
      },
      error: function(obj, st, err){
        alert(err);
      }
    });
}

save_song = function(){
    var songcontent = $("#show_lyrics_placeholder").val();
    var selected_song = $("#select_song").find(":selected").val();
    var data = {"selected_song": selected_song, "songcontent": songcontent};
    $.ajax({
        contentType: 'application/json',
        type: 'POST',
        url: 'editsavesong',
        data: JSON.stringify(data),
        success: function(d){
        if (d.success){
            send_message("Lied erfolgreich gespeichert.");
        }
        else {
            send_message("Speichern fehlgeschlagen.");
        }
        },
        error: function(obj, st, err){
            send_message(err);
        }
    });
}


$( document ).ready(function() {
    $("#all_selected_songs_placeholder").append(make_song_selector());  

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});