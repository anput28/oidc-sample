import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Response } from '../interfaces/response';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly authApi = "http://localhost:5000/api/test";

  constructor(
    private readonly http: HttpClient
  ) {}

  public secret$ = this.http.get("http://localhost:5000/api/test/secret", { withCredentials: true });

  public isAuthenticated$ = this.http.get<Response>("http://localhost:5000/api/auth/is-authenticated", { withCredentials: true });

}
