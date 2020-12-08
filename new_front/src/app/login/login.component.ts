import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth.service';
import { Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { User } from '../user';
import { throwError } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  gettoken= new User();
  error:any;
  loginform;
  constructor(private authService: AuthService,private router: Router,private fb: FormBuilder, ) { }
  ngOnInit(): void {
    this.loginform={
      username:'',
      password: '',

    };
  }
  
  login(){
    console.log(this.loginform);
    this.authService.login(this.loginform).
    subscribe(
      data1=>{
        this.gettoken = data1;
        this.router.navigate(['upload']);
      },
      error => {
        console.error('Error saving!');
        alert("not able to login");
        return throwError(error);
      }
     // success => this.router.navigate(['signup']),
    );
   }
}