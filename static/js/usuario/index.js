var $ = jQuery.noConflict();
function listadoUsuarios() {
    $.ajax({
        type: "get",
        url: "/usuario/lista_usuario",
        dataType: "json",
        success: function (response) {
            if($.fn.DataTable.isDataTable('#tabla_usuarios')){
                $('#tabla_usuarios').DataTable().destroy()
            }
            $('#tabla_usuarios tbody').html("")
            for(let i=0; i<response.length; i++){
                let fila = '<tr>'
                fila += '<td>' + (i+1) + '</td>'
                fila += '<td>' + response[i]['username'] + '</td>'
                fila += '<td>' + response[i]['email'] + '</td>'
                fila += '<td>' + response[i]['nombre'] + '</td>'
                fila += '<td>' + response[i]['apellido'] + '</td>'
                fila += '<td><button type = "button" class = "btn btn-primary btn-sm tableButton"'
                fila += 'onclick="abrir_modal_edicion(\'/usuario/editar_usuario/' + response[i]['id'] +'\')"> EDITAR </button>'
                fila += '<button type = "button" class = "btn btn-danger tableButton  btn-sm" '
                fila += 'onclick="abrir_modal_eliminacion(\'/usuario/eliminar_usuario/' + response[i]['id'] +'\')"> ELIMINAR </buttton></td>'
                fila += '</tr>'
                $('#tabla_usuarios tbody').append(fila)
            }
            $('#tabla_usuarios').DataTable({
                language: {
                    "decimal": "",
                    "emptyTable": "No hay información",
                    "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                    "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "lengthMenu": "Mostrar _MENU_ Entradas",
                    "loadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
}

// $(document).ready(function () {
//     listadoUsuarios()
// });

document.addEventListener("DOMContentLoaded", function(){
    listadoUsuarios()
});

function registrar() {
    activarBoton()
	$.ajax({
		type: $('#form_creacion').attr('method'),
		url: $('#form_creacion').attr('action'),
		data: $('#form_creacion').serialize(),
		success: function (response) {
            notificacionSuccess(response.mensaje)
			listadoUsuarios()
			cerrar_modal_creacion()
		},
		error:function (error){
			notificacionError(error.responseJSON.mensaje)
            mostrarErroresCreacion(error)
            activarBoton()
		}
	});
}

function editar() {
    activarBotonEdicion()
	$.ajax({
		type: $('#form_edicion').attr('method'),
		url: $('#form_edicion').attr('action'),
		data: $('#form_edicion').serialize(),
		success: function (response) {
            notificacionSuccess(response.mensaje)
			listadoUsuarios()
			cerrar_modal_edicion()
		},
		error:function (error){
			notificacionError(error.responseJSON.mensaje)
            mostrarErroresEdicion(error)
            activarBotonEdicion()
		}
	});
}

function eliminar(pk) {
    activarBotonEliminacion()
	$.ajax({
        data:{
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
		type: 'post',
		url: '/usuario/eliminar_usuario/'+pk,
		success: function (response) {
            notificacionSuccess(response.mensaje)
			listadoUsuarios()
			cerrar_modal_eliminacion()
		},
		error:function (error){
			notificacionError(error.responseJSON.mensaje)
            activarBotonEliminacion()
		}
	});
}