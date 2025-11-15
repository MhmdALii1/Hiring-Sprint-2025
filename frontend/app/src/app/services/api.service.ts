import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'https://hiring-sprint-2025-djkc.onrender.com/api';

  constructor(private http: HttpClient) {}

  compare(before: File, after: File): Observable<any> {
    const formData = new FormData();
    formData.append('before_image', before);
    formData.append('after_image', after);
    return this.http.post(`${this.baseUrl}/compare`, formData);
  }
}
