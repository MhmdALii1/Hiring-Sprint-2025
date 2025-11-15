import { Component, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-report',
  standalone: true,
  imports: [IonicModule, CommonModule],
  templateUrl: './report.page.html',
})
export class ReportPage implements AfterViewInit {
  report: any;

  @ViewChild('canvas') canvasRef!: ElementRef<HTMLCanvasElement>;
  private ctx!: CanvasRenderingContext2D;

  constructor(private router: Router) {
    const state = this.router.getCurrentNavigation()?.extras.state as any;
    if (state?.report) this.report = state.report;
  }

  ngAfterViewInit() {
    if (!this.report) return;

    const canvas = this.canvasRef.nativeElement;
    const img = new Image();
    img.src = this.report.after_image; // must be full URL or base64
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      this.ctx = canvas.getContext('2d')!;
      this.ctx.drawImage(img, 0, 0);

      // draw bounding boxes
      this.report.new_damages?.forEach((damage: any) => {
        const [x1, y1, x2, y2] = damage.coordinates;
        this.ctx.strokeStyle = 'red';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
        this.ctx.fillStyle = 'red';
        this.ctx.font = '14px Arial';
        this.ctx.fillText(`${damage.type}`, x1, y1 - 5);
      });
    };
  }
}
