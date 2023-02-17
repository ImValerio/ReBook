import { NgModule } from '@angular/core';
import { Route, RouterModule } from '@angular/router';
import { OverviewComponent } from './modules/overview/overview.component';
import { SearchResultComponent } from './modules/search-result/search-result.component';

export const appRoutes: Route[] = [
  { path: '', pathMatch: 'full', redirectTo: 'overview' },
  
  { 
    path: '', 
    children:[
      {path: 'overview', component: OverviewComponent ,loadChildren: () => import('./modules/overview/overview.module').then(m => m.OverviewModule)},
      {path: 'search-result/:text', component: SearchResultComponent, loadChildren: () => import('./modules/search-result/search-result.module').then(m => m.SearchResultModule) }    
    ] 
  },

];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
