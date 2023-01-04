import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputSearchComponent } from './input-search/input-search.component';
import { PageBodyComponent } from './layout/page-body/page-body.component';
import { PageHeaderComponent } from './layout/page-header/page-header.component';


@NgModule({
  declarations: [
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
  ],
  exports:[
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
  ],
  imports: [
    CommonModule,
  ]
})
export class SharedModule { }
