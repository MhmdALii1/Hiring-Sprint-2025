import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-return',
  standalone: true,
  imports: [IonicModule, CommonModule],
  templateUrl: './return.page.html',
  styleUrls: ['./return.page.scss'],
})
export class ReturnPage {
  files: File[] = [];

  constructor(private api: ApiService, private router: Router) {
    const state = this.router.getCurrentNavigation()?.extras.state as any;
    if (state?.files) {
      this.files = state.files;
    }
  }

  onFilesSelected(event: any) {
    // Explicitly cast to File[]
    this.files = Array.from(event.target.files) as File[];
  }

  get selectedFileNames(): string {
    return this.files.map((f) => f.name).join(', ');
  }

  async compare() {
    if (this.files.length < 2) {
      alert('Select before and after images.');
      return;
    }

    try {
      const report = await firstValueFrom(
        this.api.compare(this.files[0], this.files[1])
      );
      this.router.navigate(['/report'], { state: { report } });
    } catch (err) {
      console.error(err);
      alert('Error comparing images.');
    }
  }
}
