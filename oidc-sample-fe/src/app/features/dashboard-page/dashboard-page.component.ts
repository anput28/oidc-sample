import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard-page.component.html',
  styleUrls: ['./dashboard-page.component.css']
})
export class DashboardPageComponent {

  public secret = '';

  constructor(private readonly authService: AuthService) { }

  public getSecret() {
    this.authService.secret$.subscribe(resp => {
      this.secret = JSON.stringify(resp);
    })
  }

}
