/*Large Content*/
$("#modal-large").iziModal({
  title: "Welcome to the iziModal",
  subtitle: "Simple, complete and lightweight modal plugin with jquery.",
  icon: 'icon-chat',
  headerColor: '#000',
  attached: 'bottom',
  // overlayColor: 'rgba(255, 255, 255, 0.4)',
  // headerColor: '#334c7b',
  iconColor: 'white',
  fullscreen: true,
  width: 700,
  padding: 20
});
$(document).on('click', '.trigger-large', function (event) {
  event.preventDefault();
  $('#modal-large').iziModal('open');
});
/*Large Content*/