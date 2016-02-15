make_song_selector = function(){
  var div = $('<div />').addClass("placeholder_selectgroup");

  var select_song = $('<select />').addClass("class_selected_songs").css("width", "35%");
  div.append(select_song);
  $(select_song).select2({
    placeholder: "Lied"
  });

  var span_space = $('<span />').css("margin-left","5px").css("margin-right","5px");
  div.append(span_space);

  songlist.forEach(function(element){
    var option = $('<option />').text(element[1]).val(element[0]);
    option.attr('data-tonart', element[2]);
    select_song.append(option);
  });

  var select_mode = $('<select />').css("width", "10%").addClass("class_selected_modes");
  div.append(select_mode);
  $(select_mode).select2({
    placeholder: "Tonart",
    minimumResultsForSearch: Infinity
  });

  var del_button = $('<button />').addClass("btn btn-danger btn-sm").text("Entfernen").css("margin-left","9px").on("click", function() {delete_song(this);});
  div.append(del_button);
  return div;
};


delete_song = function(that){
  var div_to_delete = $(that).parent(".placeholder_selectgroup");
  div_to_delete.remove();
};


make_mode_selector = function(that){
  var tonart = $(that).select2().find(":selected").data("tonart");
  first_letter = tonart.charAt(0);
  if (first_letter == first_letter.toUpperCase()) {
    var available_modes = [tonart, "As", "Es", "B", "F", "C", "G", "D", "A", "E"];
  } else {
    var available_modes = [tonart, "f", "c", "g", "d", "a", "e", "h", "fis", "cis"];
  }
  var select_mode = $(that).parent().children(".class_selected_modes");
  select_mode.empty().trigger("change");
  available_modes.forEach(function(element){
    var option = $('<option />').text(element).val(element);
    select_mode.append(option);
  });
  $(select_mode).select2({
    minimumResultsForSearch: Infinity
  });
};


add_song_fct = function(){
  $("#all_selected_songs_placeholder").append(make_song_selector());
};


check_new_song = function(){
  var songtitle = $("#textarea_songtitle").val();
  var songcontent = $("#textarea_songcontent").val();
  var data = {"songtitle": songtitle, "songcontent": songcontent};
  $.ajax({
    contentType: 'application/json',
    type: 'POST',
    url: 'checksong',
    data: JSON.stringify(data),
    success: function(d){
      $("#show_pdf_check").remove();
      $("#show_pdf_check_placeholder").append(d.path);
    },
    error: function(obj, st, err){
      alert(err);
    }
  });
}

$( document ).ready(function() {
  $("#all_selected_songs_placeholder").append(make_song_selector());
  $("#btn_get_lyrics").click(function(){
    var selected_songs = [];
    $.each($(".class_selected_songs"), function(){
     selected_songs.push($(this).select2().find(":selected").val());
   });
    var selected_modes = [];
    $.each($(".class_selected_modes"), function(){
     selected_modes.push($(this).select2().find(":selected").val());
     $(this).select2({minimumResultsForSearch: Infinity});
   });
    var jazz = $("#checkbox-jazz").is(":checked");
    var data = {"songs": selected_songs, "modes": selected_modes, "jazz": jazz};
    $.ajax({
      contentType: 'application/json',
      type: 'POST',
      url: 'getsong',
      data: JSON.stringify(data),
      success: function(d){
        $("#show_pdf").remove();
        $("#show_pdf_placeholder").append(d.path);
      },
      error: function(obj, st, err){
        alert(err);
      }
    });
  });


  $('#all_selected_songs_placeholder').on('change', '.class_selected_songs', function(){
    make_mode_selector(this);
  });

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});