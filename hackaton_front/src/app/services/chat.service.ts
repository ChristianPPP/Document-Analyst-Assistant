import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  serviceURL : string ;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json; charset=utf-8',
    }),
  };

  constructor(private http : HttpClient) {
    this.serviceURL = "http://localhost:8000"
  }

  searchFile(body: any) {
    return this.http.post(this.serviceURL+'/api/v1/gettextprompt', body, this.httpOptions)
  }

  chat(body: any) {
    return this.http.post(this.serviceURL+'/api/v1/getresponseia', body, this.httpOptions)
  }
}
