import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { throwError } from 'rxjs';
@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  DJANGO_SERVER = 'http://127.0.0.1:8000'
  form: FormGroup;
  file_p:string;
  response;
  imageURL;
  getsome;
  num;
  constructor(private formBuilder: FormBuilder, private authService: AuthService) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      profile: ['']
    });
  }

  onChange(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.form.get('profile').setValue(file);
    }
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.form.get('profile').value);

    this.authService.upload(formData).subscribe(
      (res) => {
        this.response = res;
        this.imageURL = `${this.DJANGO_SERVER}${res.file}`;
          console.log(res);
          console.log(this.imageURL);
      },
      (err) => {  
        console.log(err);
        alert('File Upload not Successful');
      }
    );
  }
  
  logic(){
    console.log(this.response);
    this.authService.logic(this.response).
    subscribe(
      data2=>{
        this.getsome = data2;
      },
      error => {
        console.error('Error saving!');
        alert("not able to process");
        return throwError(error); 
      }
     // success => this.router.navigate(['signup']),
    );
   }

   

}
