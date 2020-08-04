// On DOM Loaded
document.addEventListener('DOMContentLoaded', function () {

    let sidenavEl = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenavEl);

    let fixedActionBtnEl = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(fixedActionBtnEl);

    let selectEl = document.querySelectorAll('select');
    M.FormSelect.init(selectEl);

    let tooltippedEl = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltippedEl);

    let collapsibleEl = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibleEl);

    let modalEl = document.querySelectorAll('.modal');
    M.Modal.init(modalEl);

    let dropdownTriggerEl = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(dropdownTriggerEl);

    let browseTabsEl = document.querySelectorAll('.tabs');
    M.Tabs.init(browseTabsEl);
});