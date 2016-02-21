take_this_mode = function(mode){
    console.log(mode)
    var data = {"mode": mode};
    $.ajax({
    contentType: 'application/json',
    type: 'POST',
    url: 'setmode',
    data: JSON.stringify(data),
    success: function(d){},
    error: function(obj, st, err){
      alert(err);
    }
  });
}


check_mode = function(songcontent){
  var songtitle = $("#textarea_songtitle").val();
  var data = {"songtitle": songtitle};
  
  $.ajax({
    contentType: 'application/json',
    type: 'POST',
    url: 'getmode',
    data: JSON.stringify(data),
    success: function(d){
      $("#btn_mode_2").remove();
      $("#btn_mode_1").remove();
      var mode1 = d.mode1;
      var mode2 = d.mode2;
      var mode1f = d.mode1f;
      var mode2f = d.mode2f;
      var btn_mode_1 = $('<button />').attr("id","btn_mode_1").addClass("btn btn-info btn-sm")
        .text(mode1f).css("margin-left","3%").on("click", function() {take_this_mode(mode1);});
      var btn_mode_2 = $('<button />').attr("id","btn_mode_2").addClass("btn btn-info btn-sm")
        .text(mode2f).css("margin-left","3%").on("click", function() {take_this_mode(mode2);});
      $("#btn_modes_placeholder").append(btn_mode_1);
      $("#btn_modes_placeholder").append(btn_mode_2);
    },
    error: function(obj, st, err){
      alert(err);
    }
  });
}


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
      $("#show_pdf_check_placeholder").append(d.path);

      var mode1 = d.mode1;
      var mode2 = d.mode2;
      $("#btn_mode_2").remove();
      $("#btn_mode_1").remove();
      var btn_mode_1 = $('<button />').prop("type","radio").attr("id","btn_mode_1").addClass("btn btn_mode_suggestion")
        .text(mode1).val(mode1).css("margin-left","1%").on("click", function() {set_selected_mode(this);});
      var btn_mode_2 = $('<button />').prop("type","radio").attr("id","btn_mode_2").addClass("btn btn_mode_suggestion")
        .text(mode2).val(mode2).css("margin-left","1%").on("click", function() {set_selected_mode(this);});
      $("#show_pdf_check").remove();
      $("#btn_modes_placeholder").append(btn_mode_1);
      $("#btn_modes_placeholder").append(btn_mode_2);
      $("#btn_modes_placeholder").removeClass("hidden");
    },
    error: function(obj, st, err){
      alert(err);
    }
  });
}

set_selected_mode = function(e) {
  $("#btn_save_song").removeClass("hidden");
  if (!$(e).hasClass('active')){
    $(e).addClass('active');
    $(e).siblings().removeClass('active');
    $(e).siblings().prop('selectedIndex', 0);
  }
}

$( document ).ready(function() {
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});