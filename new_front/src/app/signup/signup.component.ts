import { Component, OnInit } from '@angular/core';
import { throwError } from 'rxjs';
import { AuthService } from '../../auth.service';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  error:any;
  
  getinfo;
  signupform;
  //title = 'frontendssl';
  constructor(private authService: AuthService, ) { }
  ngOnInit(): void {
    this.signupform={
      username:'',
      password: '',
      first_name:'',
      last_name:''

    };
  }

  signup() {
    console.log(this.signupform);
    this.authService.post(this.signupform).
    subscribe(
      data=>{
        this.getinfo = data;
        alert("User is registered , You can login!");
      },
      error => {
        console.error('Error saving!');
        alert(" username is already taken");
        return throwError(error);
      }
    );
    
    
  }

}
