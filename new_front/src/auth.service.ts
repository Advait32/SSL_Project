import { Injectable } from '@angular/core';
import { HttpClient,HttpParams,HttpResponse , HttpInterceptor, HttpRequest, HttpHandler, HttpEvent} from '@angular/common/http';
import {Observable} from 'rxjs';
import { CanActivate, Router } from '@angular/router';
import { tap, shareReplay } from 'rxjs/operators';

import jwtDecode from "jwt-decode";
import * as moment from 'moment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  DJANGO_SERVER: string = "http://127.0.0.1:8000";
  constructor(private http: HttpClient,) { }
  post(check):Observable<any>{
    return this.http.post('http://localhost:8000/account/api/register',check)
  }
  
  login(userData):Observable<any>{
    return this.http.post('http://localhost:8000/api/token/',userData)
  }
  public upload(formData) {
    return this.http.post<any>(`${this.DJANGO_SERVER}/fileupload/`, formData);
  }
  logic(file_p:string):Observable<any>{
    return this.http.post(`${this.DJANGO_SERVER}/logic/`,{file_p})

  }



}


