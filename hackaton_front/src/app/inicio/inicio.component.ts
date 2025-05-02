import { Component, OnInit } from '@angular/core';
import { ChatService } from '../services/chat.service';

@Component({
  selector: 'app-inicio',
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {

  constructor(private chatService: ChatService) {

  }
  mensajes: { texto: string; emisor: 'sistema' | 'usuario' }[] = [];
  nuevoMensaje: string = '';
  respuestasUsuario: string[] = [];
  paso: number = 0;

  ngOnInit() {
    this.enviarMensajeSistema('Hola, ¿sobre que documento vamos a trabajar?');
  }

  enviarMensaje() {
    const mensajeUsuario = this.nuevoMensaje.trim();
    if (mensajeUsuario) {
      this.mensajes.push({ texto: mensajeUsuario, emisor: 'usuario' });
      this.respuestasUsuario.push(mensajeUsuario);
      this.nuevoMensaje = '';
      this.responderSistema(mensajeUsuario);
    }
  }

  enviarMensajeSistema(texto: string) {
    this.mensajes.push({ texto, emisor: 'sistema' });
  }

  responderSistema(msj: string) {
    this.paso++;
    if (this.paso === 1) {
      const [respuesta1] = this.respuestasUsuario;
      this.chatService.searchFile({prompt:respuesta1}).subscribe((result: any) => {
        setTimeout(() => this.enviarMensajeSistema(result.text), 500);
      })
    } else if (this.paso > 1) {
      this.chatService.chat({text: "",question: msj}).subscribe((result: any) => {
        const resumen = result.data;
        setTimeout(() => this.enviarMensajeSistema(resumen), 500);
      })
    }
  }
}
