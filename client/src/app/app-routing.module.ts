import { NgModule } from '@angular/core';
import { Route, RouterModule } from '@angular/router';
import { OverviewComponent } from './modules/overview/overview.component';

export const appRoutes: Route[] = [
  { path: '', pathMatch: 'full', redirectTo: 'overview' },
  
  
  { 
    path: '', 
    component: OverviewComponent,
    children:[{path: 'overview',loadChildren: () => import('./modules/overview/overview.module').then(m => m.OverviewModule)},] 
  }

];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
