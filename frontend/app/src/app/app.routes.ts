import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'pickup',
    loadComponent: () =>
      import('./pages/pickup/pickup.page').then((m) => m.PickupPage),
  },
  {
    path: 'report',
    loadComponent: () =>
      import('./pages/report/report.page').then((m) => m.ReportPage),
  },
  {
    path: 'return',
    loadComponent: () =>
      import('./pages/return/return.page').then((m) => m.ReturnPage),
  },
  {
    path: '',
    redirectTo: 'pickup',
    pathMatch: 'full',
  },
];
