import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-pickup',
  standalone: true,
  imports: [IonicModule, CommonModule],
  templateUrl: './pickup.page.html',
  styleUrls: ['./pickup.page.scss'],
})
export class PickupPage {
  files: File[] = [];

  constructor(private router: Router) {}

  onFilesSelected(event: any) {
    this.files = Array.from(event.target.files) as File[];
  }

  next() {
    if (this.files.length === 0) {
      alert('Select at least one file.');
      return;
    }
    this.router.navigate(['/return'], { state: { files: this.files } });
  }
}
