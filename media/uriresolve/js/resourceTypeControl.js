$(document).ready(function() {
	typeSelect = $('#id_resource_type');
	if (typeSelect.selectedIndex == 0) {
		typeSelect.empty();
	}
	
	$('#id_name_authority').change(function() {
		typeSelect.empty();
		authority = this.children[this.selectedIndex].text
		$.getJSON('/uri-gin/' + authority + '/type/json', function(data) {
			for (var index in data) {
				typeSelect.append('<option value="' + data[index].pk + '">' + authority + ': ' + data[index].fields['label'] + '</option>');
			};
		});
	});
});

