import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { OverviewRoutingModule } from './overview-routing.module';
import { OverviewComponent } from './overview.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { OverviewService } from './overview.service';


@NgModule({
  declarations: [
    OverviewComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    OverviewRoutingModule
  ],
  providers:[
    OverviewService
  ],
})
export class OverviewModule { }
